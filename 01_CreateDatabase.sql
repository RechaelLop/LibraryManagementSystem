-- ============================================
-- PHASE 1: CREATE DATABASE
-- Library Management System
-- ============================================

PRINT '============================================';
PRINT 'PHASE 1: Creating Database';
PRINT '============================================';
GO

-- Switch to master database to create new database
USE master;
GO

-- Check if database exists and drop it (for clean setup)
IF EXISTS (SELECT name FROM sys.databases WHERE name = 'LibraryManagement')
BEGIN
    PRINT '⚠️  Database "LibraryManagement" already exists.';
    PRINT '⚠️  Dropping existing database...';
    
    -- Close any open connections
    ALTER DATABASE LibraryManagement SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE LibraryManagement;
    
    PRINT '✅ Database dropped successfully!';
END
GO

-- Create the database
CREATE DATABASE LibraryManagement;
GO

PRINT '✅ Database "LibraryManagement" created successfully!';
GO

-- Switch to the new database
USE LibraryManagement;
GO

PRINT '✅ Now using "LibraryManagement" database';
GO

-- Verify we're in the right database
SELECT 
    DB_NAME() AS CurrentDatabase,
    @@VERSION AS SQLServerVersion;
GO

PRINT '============================================';
PRINT '✅ PHASE 1 COMPLETE!';
PRINT '============================================';
PRINT 'Database created: LibraryManagement';
PRINT 'Next step: Create tables (02_CreateTables.sql)';
PRINT '============================================';
GO