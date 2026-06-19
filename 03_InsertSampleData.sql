-- ============================================
-- PHASE 3: INSERT SAMPLE DATA
-- Library Management System
-- ============================================

USE LibraryManagement;
GO

PRINT '============================================';
PRINT 'PHASE 3: Inserting Sample Data';
PRINT '============================================';
GO

-- ============================================
-- 1. INSERT BOOKS
-- ============================================
PRINT 'Inserting books...';
GO

INSERT INTO books (title, author, isbn, genre, total_copies, available_copies) VALUES
('The Great Gatsby', 'F. Scott Fitzgerald', '978-0-7432-7356-5', 'Fiction', 3, 3),
('To Kill a Mockingbird', 'Harper Lee', '978-0-06-112008-4', 'Fiction', 2, 2),
('1984', 'George Orwell', '978-0-452-28423-4', 'Science Fiction', 4, 4),
('The Catcher in the Rye', 'J.D. Salinger', '978-0-316-76948-0', 'Fiction', 2, 2),
('The Hobbit', 'J.R.R. Tolkien', '978-0-547-92822-7', 'Fantasy', 3, 3),
('Pride and Prejudice', 'Jane Austen', '978-0-14-143951-8', 'Romance', 2, 2),
('The Alchemist', 'Paulo Coelho', '978-0-06-250217-4', 'Fiction', 2, 2),
('Harry Potter and the Sorcerer''s Stone', 'J.K. Rowling', '978-0-439-70818-8', 'Fantasy', 5, 5);
GO

PRINT '✅ Books inserted successfully!';
GO

-- Show the books we inserted
SELECT COUNT(*) AS TotalBooks FROM books;
GO

-- ============================================
-- 2. INSERT MEMBERS
-- ============================================
PRINT 'Inserting members...';
GO

INSERT INTO members (first_name, last_name, email, phone, membership_date, status) VALUES
('John', 'Doe', 'john.doe@email.com', '555-0101', GETDATE(), 'Active'),
('Jane', 'Smith', 'jane.smith@email.com', '555-0102', GETDATE(), 'Active'),
('Robert', 'Johnson', 'robert.j@email.com', '555-0103', GETDATE(), 'Active'),
('Emily', 'Brown', 'emily.b@email.com', '555-0104', GETDATE(), 'Active'),
('Michael', 'Davis', 'michael.d@email.com', '555-0105', GETDATE(), 'Active'),
('Sarah', 'Wilson', 'sarah.w@email.com', '555-0106', GETDATE(), 'Inactive');
GO

PRINT '✅ Members inserted successfully!';
GO

-- Show the members we inserted
SELECT COUNT(*) AS TotalMembers FROM members;
GO

-- ============================================
-- 3. INSERT BORROWING RECORDS
-- ============================================
PRINT 'Inserting borrowing records...';
GO

-- These dates are relative to today
INSERT INTO borrowing (book_id, member_id, borrow_date, due_date, return_date, status) VALUES
-- Book 1 borrowed by John (returned)
(1, 1, DATEADD(DAY, -10, GETDATE()), DATEADD(DAY, -3, GETDATE()), DATEADD(DAY, -2, GETDATE()), 'Returned'),
-- Book 2 borrowed by Jane (currently borrowed)
(2, 2, DATEADD(DAY, -5, GETDATE()), DATEADD(DAY, 9, GETDATE()), NULL, 'Borrowed'),
-- Book 3 borrowed by John (returned)
(3, 1, DATEADD(DAY, -15, GETDATE()), DATEADD(DAY, -8, GETDATE()), DATEADD(DAY, -7, GETDATE()), 'Returned'),
-- Book 4 borrowed by Robert (currently borrowed)
(4, 3, DATEADD(DAY, -3, GETDATE()), DATEADD(DAY, 11, GETDATE()), NULL, 'Borrowed'),
-- Book 5 borrowed by Michael (overdue!)
(5, 4, DATEADD(DAY, -20, GETDATE()), DATEADD(DAY, -13, GETDATE()), NULL, 'Borrowed'),
-- Book 6 borrowed by Emily (currently borrowed)
(6, 5, DATEADD(DAY, -2, GETDATE()), DATEADD(DAY, 12, GETDATE()), NULL, 'Borrowed');
GO

PRINT '✅ Borrowing records inserted successfully!';
GO

-- Show the borrowing records
SELECT COUNT(*) AS TotalBorrowings FROM borrowing;
GO

-- ============================================
-- VERIFY ALL DATA
-- ============================================
PRINT '============================================';
PRINT 'Data Summary:';
PRINT '============================================';
GO

SELECT 'Books' AS Category, COUNT(*) AS Count FROM books
UNION ALL
SELECT 'Members', COUNT(*) FROM members
UNION ALL
SELECT 'Borrowing Records', COUNT(*) FROM borrowing;
GO

-- Show sample data
PRINT '============================================';
PRINT 'Sample Books:';
PRINT '============================================';
SELECT TOP 5 book_id, title, author, genre, available_copies 
FROM books 
ORDER BY book_id;
GO

PRINT '============================================';
PRINT 'Sample Members:';
PRINT '============================================';
SELECT TOP 5 member_id, first_name, last_name, email, status 
FROM members 
ORDER BY member_id;
GO

PRINT '============================================';
PRINT 'Current Borrowings:';
PRINT '============================================';
SELECT 
    b.borrow_id,
    bk.title AS Book,
    CONCAT(m.first_name, ' ', m.last_name) AS Member,
    b.borrow_date,
    b.due_date,
    b.status,
    CASE 
        WHEN b.due_date < GETDATE() AND b.status = 'Borrowed' THEN '⚠️ OVERDUE'
        WHEN b.status = 'Borrowed' THEN '✅ Active'
        ELSE '📚 Returned'
    END AS Status_Indicator
FROM borrowing b
JOIN books bk ON b.book_id = bk.book_id
JOIN members m ON b.member_id = m.member_id
ORDER BY b.borrow_id;
GO

PRINT '============================================';
PRINT '✅ PHASE 3 COMPLETE!';
PRINT '============================================';
PRINT 'Data inserted:';
PRINT '  📚 Books: 8 titles';
PRINT '  👥 Members: 6 members';
PRINT '  📖 Borrowings: 6 transactions';
PRINT '';
PRINT 'Next step: Create stored procedures (04_CreateProcedures.sql)';
PRINT '============================================';
GO