-- ============================================
-- PHASE 5: CREATE VIEWS
-- Library Management System
-- ============================================

USE LibraryManagement;
GO

PRINT '============================================';
PRINT 'PHASE 5: Creating Views';
PRINT '============================================';
GO

-- ============================================
-- VIEW 1: Currently Borrowed Books
-- Shows all books that are currently checked out
-- ============================================
PRINT 'Creating view: CurrentlyBorrowed...';
GO

CREATE OR ALTER VIEW CurrentlyBorrowed AS
SELECT 
    b.borrow_id,
    bk.title AS BookTitle,
    bk.author,
    CONCAT(m.first_name, ' ', m.last_name) AS MemberName,
    m.email AS MemberEmail,
    m.phone AS MemberPhone,
    b.borrow_date,
    b.due_date,
    DATEDIFF(DAY, GETDATE(), b.due_date) AS DaysRemaining,
    CASE 
        WHEN b.due_date < GETDATE() THEN '?? OVERDUE'
        WHEN DATEDIFF(DAY, GETDATE(), b.due_date) <= 3 THEN '?? Due Soon'
        WHEN DATEDIFF(DAY, GETDATE(), b.due_date) <= 7 THEN '?? Due This Week'
        ELSE '?? On Time'
    END AS StatusAlert
FROM borrowing b
JOIN books bk ON b.book_id = bk.book_id
JOIN members m ON b.member_id = m.member_id
WHERE b.status = 'Borrowed';
GO

PRINT '? CurrentlyBorrowed view created!';
GO

-- ============================================
-- VIEW 2: Overdue Books
-- Shows all books that are past their due date
-- ============================================
PRINT 'Creating view: OverdueBooks...';
GO

CREATE OR ALTER VIEW OverdueBooks AS
SELECT 
    b.borrow_id,
    bk.title AS BookTitle,
    bk.author,
    bk.isbn,
    CONCAT(m.first_name, ' ', m.last_name) AS MemberName,
    m.email AS MemberEmail,
    m.phone AS MemberPhone,
    b.borrow_date,
    b.due_date,
    DATEDIFF(DAY, b.due_date, GETDATE()) AS DaysOverdue,
    ROUND(DATEDIFF(DAY, b.due_date, GETDATE()) * 0.50, 2) AS EstimatedFine,
    CONCAT('$', ROUND(DATEDIFF(DAY, b.due_date, GETDATE()) * 0.50, 2)) AS FineAmount
FROM borrowing b
JOIN books bk ON b.book_id = bk.book_id
JOIN members m ON b.member_id = m.member_id
WHERE b.status = 'Borrowed' 
AND b.due_date < GETDATE()
ORDER BY b.due_date ASC;
GO

PRINT '? OverdueBooks view created!';
GO

-- ============================================
-- VIEW 3: Book Popularity
-- Shows most borrowed books
-- ============================================
PRINT 'Creating view: BookPopularity...';
GO

CREATE OR ALTER VIEW BookPopularity AS
SELECT 
    bk.book_id,
    bk.title,
    bk.author,
    bk.genre,
    COUNT(b.borrow_id) AS TotalBorrows,
    bk.total_copies,
    bk.available_copies,
    CASE 
        WHEN COUNT(b.borrow_id) >= 3 THEN '?? Very Popular'
        WHEN COUNT(b.borrow_id) >= 1 THEN '?? Popular'
        ELSE '?? Available'
    END AS PopularityRating,
    CASE 
        WHEN bk.available_copies = 0 THEN 'Out of Stock'
        WHEN bk.available_copies <= 2 THEN 'Low Stock'
        ELSE 'In Stock'
    END AS StockStatus
FROM books bk
LEFT JOIN borrowing b ON bk.book_id = b.book_id
GROUP BY bk.book_id, bk.title, bk.author, bk.genre, bk.total_copies, bk.available_copies;
GO

PRINT '? BookPopularity view created!';
GO

-- ============================================
-- VIEW 4: Member Activity Summary
-- Shows borrowing statistics for each member
-- ============================================
PRINT 'Creating view: MemberActivity...';
GO

CREATE OR ALTER VIEW MemberActivity AS
SELECT 
    m.member_id,
    CONCAT(m.first_name, ' ', m.last_name) AS MemberName,
    m.email,
    m.phone,
    m.status AS MemberStatus,
    m.membership_date,
    COUNT(b.borrow_id) AS TotalBorrows,
    SUM(CASE WHEN b.status = 'Borrowed' THEN 1 ELSE 0 END) AS CurrentBorrows,
    SUM(CASE WHEN b.status = 'Borrowed' AND b.due_date < GETDATE() THEN 1 ELSE 0 END) AS OverdueBooks,
    ISNULL(SUM(b.fine_amount), 0) AS TotalFines,
    CASE 
        WHEN SUM(CASE WHEN b.status = 'Borrowed' AND b.due_date < GETDATE() THEN 1 ELSE 0 END) > 0 THEN '?? Has Overdue Books'
        WHEN SUM(CASE WHEN b.status = 'Borrowed' THEN 1 ELSE 0 END) > 0 THEN '?? Active Borrower'
        WHEN COUNT(b.borrow_id) > 0 THEN '?? Past Borrower'
        ELSE '? No Activity'
    END AS MemberActivityStatus
FROM members m
LEFT JOIN borrowing b ON m.member_id = b.member_id
GROUP BY m.member_id, m.first_name, m.last_name, m.email, m.phone, m.status, m.membership_date;
GO

PRINT '? MemberActivity view created!';
GO

-- ============================================
-- VIEW 5: Library Statistics Dashboard
-- Single view with summary statistics
-- ============================================
PRINT 'Creating view: LibraryStats...';
GO

CREATE OR ALTER VIEW LibraryStats AS
SELECT 
    (SELECT COUNT(*) FROM books) AS TotalBooks,
    (SELECT SUM(total_copies) FROM books) AS TotalCopies,
    (SELECT SUM(available_copies) FROM books) AS AvailableCopies,
    (SELECT COUNT(*) FROM members) AS TotalMembers,
    (SELECT COUNT(*) FROM members WHERE status = 'Active') AS ActiveMembers,
    (SELECT COUNT(*) FROM borrowing WHERE status = 'Borrowed') AS CurrentlyBorrowed,
    (SELECT COUNT(*) FROM borrowing WHERE status = 'Borrowed' AND due_date < GETDATE()) AS OverdueBooks,
    (SELECT ISNULL(SUM(fine_amount), 0) FROM borrowing) AS TotalFinesCollected,
    (SELECT COUNT(*) FROM borrowing) AS TotalTransactions,
    (SELECT COUNT(*) FROM borrowing WHERE status = 'Returned') AS CompletedReturns;
GO

PRINT '? LibraryStats view created!';
GO

-- ============================================
-- VERIFY VIEWS
-- ============================================
PRINT '============================================';
PRINT 'Verifying views...';
PRINT '============================================';
GO

SELECT 
    TABLE_NAME AS ViewName,
    TABLE_TYPE
FROM INFORMATION_SCHEMA.VIEWS
WHERE TABLE_SCHEMA = 'dbo'
ORDER BY TABLE_NAME;
GO

-- ============================================
-- DEMONSTRATE VIEWS
-- ============================================
PRINT '============================================';
PRINT 'Testing views...';
PRINT '============================================';
GO

PRINT '1. Currently Borrowed Books:';
SELECT TOP 5 * FROM CurrentlyBorrowed;
GO

PRINT '2. Overdue Books:';
SELECT TOP 5 * FROM OverdueBooks;
GO

PRINT '3. Book Popularity:';
SELECT TOP 5 * FROM BookPopularity ORDER BY TotalBorrows DESC;
GO

PRINT '4. Member Activity:';
SELECT TOP 5 * FROM MemberActivity ORDER BY TotalBorrows DESC;
GO

PRINT '5. Library Statistics Dashboard:';
SELECT * FROM LibraryStats;
GO

-- ============================================
-- SAMPLE QUERIES USING VIEWS
-- ============================================
PRINT '============================================';
PRINT 'Sample queries using views:';
PRINT '============================================';
GO

-- Query 1: Members with overdue books
PRINT 'Members with overdue books:';
SELECT MemberName, email, OverdueBooks, TotalFines
FROM MemberActivity
WHERE OverdueBooks > 0
ORDER BY OverdueBooks DESC;
GO

-- Query 2: Popularity of books by genre
PRINT 'Average borrows per genre:';
SELECT 
    genre,
    COUNT(*) AS BookCount,
    SUM(TotalBorrows) AS TotalBorrows,
    AVG(TotalBorrows) AS AvgBorrowsPerBook
FROM BookPopularity
GROUP BY genre
ORDER BY AvgBorrowsPerBook DESC;
GO

-- Query 3: Books that need restocking
PRINT 'Books needing restocking:';
SELECT title, author, total_copies, available_copies
FROM BookPopularity
WHERE available_copies <= 2 AND total_copies > 0
ORDER BY available_copies ASC;
GO

-- Query 4: Library health check
PRINT 'Library Health Check:';
SELECT 
    TotalBooks,
    AvailableCopies,
    TotalMembers,
    ActiveMembers,
    CurrentlyBorrowed,
    OverdueBooks,
    TotalFinesCollected,
    ROUND(CAST(AvailableCopies AS FLOAT) / TotalCopies * 100, 2) AS AvailabilityPercentage
FROM LibraryStats;
GO

PRINT '============================================';
PRINT '? PHASE 5 COMPLETE!';
PRINT '============================================';
PRINT 'Views created:';
PRINT '  1. CurrentlyBorrowed  - Current borrowings with status alerts';
PRINT '  2. OverdueBooks       - All overdue books with fines';
PRINT '  3. BookPopularity     - Most borrowed books with ratings';
PRINT '  4. MemberActivity     - Member borrowing statistics';
PRINT '  5. LibraryStats       - Overall library dashboard';
PRINT '';
PRINT 'Next step: Test everything (06_TestQueries.sql)';
PRINT '============================================';
GO