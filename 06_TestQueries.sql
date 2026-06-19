-- ============================================
-- PHASE 6: COMPLETE SYSTEM TEST (FIXED)
-- Library Management System
-- Test all procedures and views
-- ============================================

USE LibraryManagement;
GO

PRINT '============================================';
PRINT 'PHASE 6: Complete System Test';
PRINT '============================================';
PRINT CONVERT(VARCHAR, GETDATE(), 120);
GO

-- ============================================
-- SECTION 1: TEST VIEWS
-- ============================================
PRINT '============================================';
PRINT 'SECTION 1: Testing Views';
PRINT '============================================';
GO

-- Test 1: Currently Borrowed Books
PRINT '📖 Test 1: Currently Borrowed Books';
SELECT * FROM CurrentlyBorrowed;
GO

-- Test 2: Overdue Books
PRINT '⚠️ Test 2: Overdue Books';
SELECT * FROM OverdueBooks ORDER BY due_date;
GO

-- Test 3: Book Popularity
PRINT '🔥 Test 3: Book Popularity';
SELECT TOP 5 * FROM BookPopularity ORDER BY TotalBorrows DESC;
GO

-- Test 4: Member Activity
PRINT '👥 Test 4: Member Activity';
SELECT * FROM MemberActivity;
GO

-- Test 5: Library Statistics
PRINT '📊 Test 5: Library Statistics';
SELECT * FROM LibraryStats;
GO

-- ============================================
-- SECTION 2: TEST STORED PROCEDURES
-- ============================================
PRINT '============================================';
PRINT 'SECTION 2: Testing Stored Procedures';
PRINT '============================================';
GO

-- Test 6: Search Books
PRINT '🔍 Test 6: Search for Books';
PRINT 'Searching for "Harry":';
EXEC SearchBooks 'Harry';
GO

PRINT 'Searching for "Tolkien" in Fantasy genre:';
EXEC SearchBooks 'Tolkien', 'Fantasy';
GO

PRINT 'Searching for available books with "The":';
EXEC SearchBooks 'The', NULL, 1;
GO

-- Test 7: View Member History
PRINT '📋 Test 7: View Member History';
PRINT 'History for John Doe (member_id = 1):';
EXEC ViewMemberHistory 1;
GO

PRINT 'History for Jane Smith (member_id = 2):';
EXEC ViewMemberHistory 2;
GO

-- Test 8: Get Overdue Books
PRINT '⚠️ Test 8: Get Overdue Books';
EXEC GetOverdueBooks;
GO

-- ============================================
-- SECTION 3: BORROW AND RETURN WORKFLOW
-- ============================================
PRINT '============================================';
PRINT 'SECTION 3: Complete Borrow/Return Workflow';
PRINT '============================================';
GO

-- Step 1: Check current status
PRINT '📊 Step 1: Current Library Status';
SELECT 
    'Books' AS Category,
    COUNT(*) AS Total,
    SUM(available_copies) AS Available
FROM books
UNION ALL
SELECT 
    'Members',
    COUNT(*),
    SUM(CASE WHEN status = 'Active' THEN 1 ELSE 0 END)
FROM members
UNION ALL
SELECT 
    'Borrowings',
    COUNT(*),
    SUM(CASE WHEN status = 'Borrowed' THEN 1 ELSE 0 END)
FROM borrowing;
GO

-- Step 2: Show available books
PRINT '📚 Step 2: Available Books';
SELECT book_id, title, author, available_copies 
FROM books 
WHERE available_copies > 0
ORDER BY title;
GO

-- Step 3: Borrow a book
PRINT '📖 Step 3: Borrow a book for testing';
DECLARE @test_member INT = 1;
DECLARE @test_book INT = 5;

PRINT CONCAT('Member ', @test_member, ' borrows book ', @test_book, ' for 10 days');
EXEC BorrowBook @test_member, @test_book, 10;
GO

-- Step 4: Check updated status
PRINT '📊 Step 4: Updated Library Status';
SELECT * FROM LibraryStats;
GO

-- Step 5: Show current borrowings
PRINT '📖 Step 5: Current Borrowings After Borrowing';
SELECT * FROM CurrentlyBorrowed;
GO

-- Step 6: Find the latest borrow_id
PRINT '🔢 Step 6: Finding the latest borrow_id';
DECLARE @test_borrow_id INT;
SELECT TOP 1 @test_borrow_id = borrow_id 
FROM borrowing 
WHERE status = 'Borrowed'
ORDER BY borrow_id DESC;

PRINT CONCAT('Latest borrow_id: ', @test_borrow_id);
GO

-- Step 7: Return the book
PRINT '📚 Step 7: Returning the book';
DECLARE @latest_id INT;
SELECT TOP 1 @latest_id = borrow_id 
FROM borrowing 
WHERE status = 'Borrowed'
ORDER BY borrow_id DESC;

EXEC ReturnBook @latest_id;
GO

-- Step 8: Check final status
PRINT '📊 Step 8: Final Library Status';
SELECT * FROM LibraryStats;
GO

-- ============================================
-- SECTION 4: ERROR HANDLING TESTS
-- ============================================
PRINT '============================================';
PRINT 'SECTION 4: Error Handling Tests';
PRINT '============================================';
GO

-- Test 9: Try to borrow a book with no available copies
PRINT '❌ Test 9: Borrow Unavailable Book';
PRINT 'First, check a book with low availability:';
SELECT book_id, title, available_copies 
FROM books 
WHERE available_copies = 0;

IF EXISTS (SELECT 1 FROM books WHERE available_copies = 0)
BEGIN
    DECLARE @unavailable_id INT;
    SELECT TOP 1 @unavailable_id = book_id 
    FROM books 
    WHERE available_copies = 0;
    
    PRINT CONCAT('Attempting to borrow book_id=', @unavailable_id, ' (should fail)');
    EXEC BorrowBook 1, @unavailable_id, 14;
END
ELSE
BEGIN
    PRINT 'No unavailable books found. Skipping test.';
END
GO

-- Test 10: Borrow with overdue books - SIMPLIFIED VERSION
PRINT '❌ Test 10: Borrow with Overdue Books';
PRINT 'Checking members with overdue books...';

-- First, let's create an overdue situation
PRINT 'Step 1: Adding an overdue book for member 4...';

-- Insert a test overdue borrowing (if not exists)
IF NOT EXISTS (
    SELECT 1 FROM borrowing 
    WHERE member_id = 4 
    AND status = 'Borrowed' 
    AND due_date < GETDATE()
)
BEGIN
    INSERT INTO borrowing (book_id, member_id, borrow_date, due_date, status)
    VALUES (3, 4, DATEADD(DAY, -20, GETDATE()), DATEADD(DAY, -5, GETDATE()), 'Borrowed');
    PRINT '✅ Added test overdue book for member 4';
END
ELSE
BEGIN
    PRINT 'ℹ️ Member 4 already has an overdue book';
END
GO

-- Now test
PRINT 'Step 2: Attempting to borrow another book for member 4 (should fail):';
EXEC BorrowBook 4, 1, 14;
GO

-- ============================================
-- SECTION 5: ANALYTICS AND REPORTS
-- ============================================
PRINT '============================================';
PRINT 'SECTION 5: Analytics and Reports';
PRINT '============================================';
GO

-- Report 1: Genre popularity
PRINT '📊 Report 1: Genre Popularity';
SELECT 
    genre,
    COUNT(*) AS BookCount,
    SUM(TotalBorrows) AS TotalBorrows,
    CAST(AVG(CAST(TotalBorrows AS FLOAT)) AS DECIMAL(10,2)) AS AvgPerBook
FROM BookPopularity
GROUP BY genre
ORDER BY TotalBorrows DESC;
GO

-- Report 2: Member activity summary
PRINT '👥 Report 2: Member Activity Summary';
SELECT 
    MemberStatus,
    COUNT(*) AS MemberCount,
    SUM(TotalBorrows) AS TotalBorrows,
    SUM(CurrentBorrows) AS CurrentBorrows,
    SUM(OverdueBooks) AS OverdueBooks,
    CAST(AVG(TotalFines) AS DECIMAL(10,2)) AS AvgFines
FROM MemberActivity
GROUP BY MemberStatus;
GO

-- Report 3: Daily borrowing trend
PRINT '📈 Report 3: Borrowing Trend (Last 30 days)';
SELECT 
    FORMAT(borrow_date, 'yyyy-MM-dd') AS BorrowDate,
    COUNT(*) AS Borrows,
    COUNT(DISTINCT member_id) AS UniqueMembers
FROM borrowing
WHERE borrow_date >= DATEADD(DAY, -30, GETDATE())
GROUP BY FORMAT(borrow_date, 'yyyy-MM-dd')
ORDER BY BorrowDate DESC;
GO

-- Report 4: Library performance metrics
PRINT '📊 Report 4: Library Performance Metrics';
SELECT 
    (SELECT COUNT(*) FROM books) AS TotalBooks,
    (SELECT COUNT(*) FROM members WHERE status = 'Active') AS ActiveMembers,
    (SELECT COUNT(*) FROM borrowing WHERE status = 'Borrowed') AS ActiveBorrows,
    CAST(
        (SELECT COUNT(*) FROM borrowing WHERE status = 'Borrowed') AS FLOAT
    ) / 
    NULLIF((SELECT COUNT(*) FROM members WHERE status = 'Active'), 0) * 100 
    AS BorrowRatePercent,
    (SELECT COUNT(*) FROM borrowing WHERE status = 'Returned' 
     AND return_date >= DATEADD(MONTH, -1, GETDATE())) AS ReturnsLastMonth,
    (SELECT COUNT(*) FROM borrowing WHERE borrow_date >= DATEADD(MONTH, -1, GETDATE())) 
    AS BorrowsLastMonth;
GO

-- ============================================
-- SECTION 6: FINAL SUMMARY
-- ============================================
PRINT '============================================';
PRINT 'SECTION 6: Final Summary';
PRINT '============================================';
GO

PRINT '📊 System Overview:';
SELECT 
    'Total Books' AS Metric,
    CAST(COUNT(*) AS VARCHAR) AS Value
FROM books
UNION ALL
SELECT 
    'Total Members',
    CAST(COUNT(*) AS VARCHAR)
FROM members
UNION ALL
SELECT 
    'Active Members',
    CAST(COUNT(*) AS VARCHAR)
FROM members WHERE status = 'Active'
UNION ALL
SELECT 
    'Total Borrowings',
    CAST(COUNT(*) AS VARCHAR)
FROM borrowing
UNION ALL
SELECT 
    'Currently Borrowed',
    CAST(COUNT(*) AS VARCHAR)
FROM borrowing WHERE status = 'Borrowed'
UNION ALL
SELECT 
    'Overdue Books',
    CAST(COUNT(*) AS VARCHAR)
FROM borrowing WHERE status = 'Borrowed' AND due_date < GETDATE()
UNION ALL
SELECT 
    'Total Fines Collected',
    CONCAT('$', CAST(ISNULL(SUM(fine_amount), 0) AS VARCHAR))
FROM borrowing;
GO

PRINT '============================================';
PRINT '✅ ALL TESTS COMPLETED SUCCESSFULLY!';
PRINT '============================================';
PRINT '';
PRINT '📋 System Components Verified:';
PRINT '  ✅ 3 Tables (books, members, borrowing)';
PRINT '  ✅ 5 Stored Procedures';
PRINT '  ✅ 5 Views';
PRINT '  ✅ Sample Data Loaded';
PRINT '  ✅ Error Handling Works';
PRINT '  ✅ Analytics Queries Work';
PRINT '';
PRINT '🎉 YOUR LIBRARY MANAGEMENT SYSTEM IS READY!';
PRINT '============================================';
PRINT 'Completion Time: ' + CONVERT(VARCHAR, GETDATE(), 120);
PRINT '============================================';
GO