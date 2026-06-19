-- ============================================
-- PHASE 4: CREATE STORED PROCEDURES
-- Library Management System
-- ============================================

USE LibraryManagement;
GO

PRINT '============================================';
PRINT 'PHASE 4: Creating Stored Procedures';
PRINT '============================================';
GO

-- ============================================
-- PROCEDURE 1: Borrow a Book (COMPLETELY REWRITTEN)
-- ============================================
PRINT 'Creating procedure: BorrowBook...';
GO

CREATE OR ALTER PROCEDURE BorrowBook
    @member_id INT,
    @book_id INT,
    @days_to_borrow INT = 14
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @available INT;
    DECLARE @member_status NVARCHAR(20);
    DECLARE @due_date DATE;
    DECLARE @error_message NVARCHAR(200);
    DECLARE @has_overdue INT;
    
    -- Check if member is active
    SELECT @member_status = status 
    FROM members 
    WHERE member_id = @member_id;
    
    IF @member_status != 'Active'
    BEGIN
        SELECT '❌ ERROR: Member is not active' AS Message;
        RETURN;
    END
    
    -- Check if member has overdue books
    SELECT @has_overdue = COUNT(*)
    FROM borrowing 
    WHERE member_id = @member_id 
    AND status = 'Borrowed' 
    AND due_date < GETDATE();
    
    IF @has_overdue > 0
    BEGIN
        SELECT '❌ ERROR: Member has overdue books. Please return them first.' AS Message;
        RETURN;
    END
    
    -- Check book availability
    SELECT @available = available_copies 
    FROM books 
    WHERE book_id = @book_id;
    
    IF @available < 1
    BEGIN
        SELECT '❌ ERROR: No copies available for this book' AS Message;
        RETURN;
    END
    
    -- Start transaction for the actual borrow
    BEGIN TRANSACTION;
    
    BEGIN TRY
        -- Borrow the book
        SET @due_date = DATEADD(DAY, @days_to_borrow, GETDATE());
        
        INSERT INTO borrowing (book_id, member_id, borrow_date, due_date, status)
        VALUES (@book_id, @member_id, GETDATE(), @due_date, 'Borrowed');
        
        -- Update available copies
        UPDATE books 
        SET available_copies = available_copies - 1 
        WHERE book_id = @book_id;
        
        COMMIT TRANSACTION;
        
        -- Show success message
        SELECT 
            '✅ Book borrowed successfully!' AS Message,
            @due_date AS DueDate,
            @days_to_borrow AS DaysAllowed;
        
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;
            
        SELECT 
            '❌ ERROR: ' + ERROR_MESSAGE() AS Message,
            ERROR_LINE() AS ErrorLine;
    END CATCH
END
GO

PRINT '✅ BorrowBook procedure created!';
GO

-- ============================================
-- PROCEDURE 2: Return a Book
-- ============================================
PRINT 'Creating procedure: ReturnBook...';
GO

CREATE OR ALTER PROCEDURE ReturnBook
    @borrow_id INT
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @book_id INT;
    DECLARE @member_id INT;
    DECLARE @due_date DATE;
    DECLARE @days_overdue INT;
    DECLARE @fine DECIMAL(10,2);
    DECLARE @borrow_status NVARCHAR(20);
    
    BEGIN TRY
        BEGIN TRANSACTION;
        
        -- 1. Get borrowing details
        SELECT @book_id = book_id, 
               @member_id = member_id, 
               @due_date = due_date,
               @borrow_status = status
        FROM borrowing 
        WHERE borrow_id = @borrow_id;
        
        IF @book_id IS NULL
        BEGIN
            SELECT '❌ ERROR: Invalid borrow ID' AS Message;
            RETURN;
        END
        
        IF @borrow_status = 'Returned'
        BEGIN
            SELECT '❌ ERROR: This book has already been returned' AS Message;
            RETURN;
        END
        
        -- 2. Calculate fine if overdue
        SET @days_overdue = DATEDIFF(DAY, @due_date, GETDATE());
        
        IF @days_overdue > 0
            SET @fine = @days_overdue * 0.50; -- $0.50 per day
        ELSE
            SET @fine = 0;
        
        -- 3. Update borrowing record
        UPDATE borrowing 
        SET return_date = GETDATE(), 
            status = 'Returned',
            fine_amount = @fine
        WHERE borrow_id = @borrow_id;
        
        -- 4. Increase available copies
        UPDATE books 
        SET available_copies = available_copies + 1 
        WHERE book_id = @book_id;
        
        COMMIT TRANSACTION;
        
        -- 5. Show result
        IF @fine > 0
            SELECT 
                '✅ Book returned with fine!' AS Message,
                @fine AS FineAmount,
                @days_overdue AS DaysOverdue,
                'Please pay fine at the library desk.' AS Instruction;
        ELSE
            SELECT 
                '✅ Book returned successfully! No fine.' AS Message,
                0 AS FineAmount,
                0 AS DaysOverdue;
            
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        SELECT 
            '❌ ERROR: ' + ERROR_MESSAGE() AS Message,
            ERROR_LINE() AS ErrorLine;
    END CATCH
END
GO

PRINT '✅ ReturnBook procedure created!';
GO

-- ============================================
-- PROCEDURE 3: View Member History
-- ============================================
PRINT 'Creating procedure: ViewMemberHistory...';
GO

CREATE OR ALTER PROCEDURE ViewMemberHistory
    @member_id INT
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Check if member exists
    IF NOT EXISTS (SELECT 1 FROM members WHERE member_id = @member_id)
    BEGIN
        SELECT '❌ ERROR: Member not found' AS Message;
        RETURN;
    END
    
    -- Get member info
    SELECT 
        CONCAT(first_name, ' ', last_name) AS MemberName,
        email,
        phone,
        status,
        membership_date
    FROM members
    WHERE member_id = @member_id;
    
    -- Get borrowing history
    SELECT 
        b.borrow_id,
        bk.title AS BookTitle,
        bk.author,
        b.borrow_date,
        b.due_date,
        b.return_date,
        b.status,
        b.fine_amount,
        CASE 
            WHEN b.status = 'Borrowed' AND b.due_date < GETDATE() THEN '⚠️ OVERDUE'
            WHEN b.status = 'Borrowed' THEN '📖 Currently Borrowed'
            WHEN b.status = 'Returned' AND b.fine_amount > 0 THEN '💰 Returned with Fine'
            ELSE '📚 Returned'
        END AS StatusDescription
    FROM borrowing b
    JOIN books bk ON b.book_id = bk.book_id
    WHERE b.member_id = @member_id
    ORDER BY b.borrow_date DESC;
    
    -- Summary statistics
    SELECT 
        COUNT(*) AS TotalBorrowings,
        SUM(CASE WHEN status = 'Borrowed' THEN 1 ELSE 0 END) AS CurrentBorrowings,
        SUM(CASE WHEN status = 'Borrowed' AND due_date < GETDATE() THEN 1 ELSE 0 END) AS OverdueCount,
        ISNULL(SUM(fine_amount), 0) AS TotalFines
    FROM borrowing
    WHERE member_id = @member_id;
END
GO

PRINT '✅ ViewMemberHistory procedure created!';
GO

-- ============================================
-- PROCEDURE 4: Search Books
-- ============================================
PRINT 'Creating procedure: SearchBooks...';
GO

CREATE OR ALTER PROCEDURE SearchBooks
    @search_term NVARCHAR(100),
    @genre NVARCHAR(50) = NULL,
    @available_only BIT = 0
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT 
        book_id,
        title,
        author,
        isbn,
        genre,
        total_copies,
        available_copies,
        CASE 
            WHEN available_copies = 0 THEN '❌ Out of Stock'
            WHEN available_copies <= 2 THEN '⚠️ Low Stock'
            ELSE '✅ Available'
        END AS AvailabilityStatus,
        created_at
    FROM books
    WHERE 
        (title LIKE '%' + @search_term + '%' 
         OR author LIKE '%' + @search_term + '%'
         OR isbn LIKE '%' + @search_term + '%')
        AND (@genre IS NULL OR genre = @genre)
        AND (@available_only = 0 OR available_copies > 0)
    ORDER BY 
        CASE 
            WHEN title LIKE @search_term + '%' THEN 1
            WHEN author LIKE @search_term + '%' THEN 2
            ELSE 3
        END,
        title;
END
GO

PRINT '✅ SearchBooks procedure created!';
GO

-- ============================================
-- PROCEDURE 5: Get Overdue Books
-- ============================================
PRINT 'Creating procedure: GetOverdueBooks...';
GO

CREATE OR ALTER PROCEDURE GetOverdueBooks
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT 
        b.borrow_id,
        bk.title AS BookTitle,
        bk.author,
        CONCAT(m.first_name, ' ', m.last_name) AS MemberName,
        m.email,
        m.phone,
        b.due_date,
        DATEDIFF(DAY, b.due_date, GETDATE()) AS DaysOverdue,
        ROUND(DATEDIFF(DAY, b.due_date, GETDATE()) * 0.50, 2) AS EstimatedFine
    FROM borrowing b
    JOIN books bk ON b.book_id = bk.book_id
    JOIN members m ON b.member_id = m.member_id
    WHERE b.status = 'Borrowed' 
    AND b.due_date < GETDATE()
    ORDER BY b.due_date ASC;
END
GO

PRINT '✅ GetOverdueBooks procedure created!';
GO

-- ============================================
-- VERIFY PROCEDURES
-- ============================================
PRINT '============================================';
PRINT 'Verifying procedures...';
PRINT '============================================';
GO

SELECT 
    SPECIFIC_NAME AS ProcedureName,
    ROUTINE_DEFINITION
FROM INFORMATION_SCHEMA.ROUTINES
WHERE ROUTINE_TYPE = 'PROCEDURE'
AND ROUTINE_SCHEMA = 'dbo'
ORDER BY SPECIFIC_NAME;
GO

PRINT '============================================';
PRINT '✅ PHASE 4 COMPLETE!';
PRINT '============================================';
PRINT 'Stored procedures created:';
PRINT '  1. BorrowBook      - Borrow a book';
PRINT '  2. ReturnBook      - Return a book';
PRINT '  3. ViewMemberHistory - View member borrowing history';
PRINT '  4. SearchBooks     - Search for books';
PRINT '  5. GetOverdueBooks - Get all overdue books';
PRINT '';
PRINT 'Next step: Test the procedures (06_TestQueries.sql)';
PRINT '============================================';
GO