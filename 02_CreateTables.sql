-- ============================================
-- PHASE 2: CREATE TABLES
-- Library Management System
-- ============================================

USE LibraryManagement;
GO

PRINT '============================================';
PRINT 'PHASE 2: Creating Tables';
PRINT '============================================';
GO

-- Drop tables if they exist (for clean setup)
IF OBJECT_ID('borrowing', 'U') IS NOT NULL 
    DROP TABLE borrowing;
GO

IF OBJECT_ID('books', 'U') IS NOT NULL 
    DROP TABLE books;
GO

IF OBJECT_ID('members', 'U') IS NOT NULL 
    DROP TABLE members;
GO

PRINT '✅ Cleaned up old tables (if any)';
GO

-- ============================================
-- TABLE 1: BOOKS
-- ============================================
PRINT 'Creating books table...';
GO

CREATE TABLE books (
    book_id INT IDENTITY(1,1) PRIMARY KEY,
    title NVARCHAR(200) NOT NULL,
    author NVARCHAR(100) NOT NULL,
    isbn NVARCHAR(20) UNIQUE,
    genre NVARCHAR(50),
    total_copies INT DEFAULT 1,
    available_copies INT DEFAULT 1,
    created_at DATETIME DEFAULT GETDATE()
);
GO

PRINT '✅ books table created!';
GO

-- ============================================
-- TABLE 2: MEMBERS
-- ============================================
PRINT 'Creating members table...';
GO

CREATE TABLE members (
    member_id INT IDENTITY(1,1) PRIMARY KEY,
    first_name NVARCHAR(50) NOT NULL,
    last_name NVARCHAR(50) NOT NULL,
    email NVARCHAR(100) UNIQUE NOT NULL,
    phone NVARCHAR(20),
    membership_date DATE DEFAULT GETDATE(),
    status NVARCHAR(20) DEFAULT 'Active',
    CONSTRAINT CHK_MemberStatus CHECK (status IN ('Active', 'Inactive'))
);
GO

PRINT '✅ members table created!';
GO

-- ============================================
-- TABLE 3: BORROWING
-- ============================================
PRINT 'Creating borrowing table...';
GO

CREATE TABLE borrowing (
    borrow_id INT IDENTITY(1,1) PRIMARY KEY,
    book_id INT NOT NULL,
    member_id INT NOT NULL,
    borrow_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE NULL,
    status NVARCHAR(20) DEFAULT 'Borrowed',
    fine_amount DECIMAL(10,2) DEFAULT 0.00,
    CONSTRAINT CHK_BorrowStatus CHECK (status IN ('Borrowed', 'Returned')),
    CONSTRAINT FK_Borrowing_Books FOREIGN KEY (book_id) REFERENCES books(book_id),
    CONSTRAINT FK_Borrowing_Members FOREIGN KEY (member_id) REFERENCES members(member_id)
);
GO

PRINT '✅ borrowing table created!';
GO

-- ============================================
-- CREATE INDEXES FOR PERFORMANCE
-- ============================================
PRINT 'Creating indexes for better performance...';
GO

CREATE INDEX IX_borrowing_member_id ON borrowing(member_id);
CREATE INDEX IX_borrowing_book_id ON borrowing(book_id);
CREATE INDEX IX_borrowing_status ON borrowing(status);
CREATE INDEX IX_borrowing_due_date ON borrowing(due_date);
CREATE INDEX IX_books_title ON books(title);
CREATE INDEX IX_books_author ON books(author);
CREATE INDEX IX_members_email ON members(email);
GO

PRINT '✅ Indexes created!';
GO

-- ============================================
-- VERIFY TABLES
-- ============================================
PRINT '============================================';
PRINT 'Verifying tables...';
PRINT '============================================';
GO

SELECT 
    TABLE_NAME,
    TABLE_TYPE
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'dbo'
ORDER BY TABLE_NAME;
GO

-- Show table structures
PRINT '============================================';
PRINT 'books table structure:';
PRINT '============================================';
EXEC sp_help 'books';
GO

PRINT '============================================';
PRINT 'members table structure:';
PRINT '============================================';
EXEC sp_help 'members';
GO

PRINT '============================================';
PRINT 'borrowing table structure:';
PRINT '============================================';
EXEC sp_help 'borrowing';
GO

PRINT '============================================';
PRINT '✅ PHASE 2 COMPLETE!';
PRINT '============================================';
PRINT 'Tables created:';
PRINT '  📚 books';
PRINT '  👥 members';
PRINT '  📖 borrowing';
PRINT '';
PRINT 'Next step: Insert sample data (03_InsertSampleData.sql)';
PRINT '============================================';
GO