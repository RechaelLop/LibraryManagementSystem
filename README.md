# ?? Library Management System

A complete Library Management System built with **Microsoft SQL Server** that demonstrates database design, T-SQL programming, and data management skills.


---

## Overview

This Library Management System is a fully functional database application that manages:
- ?? Books inventory
- ?? Library members
- ?? Borrowing and returning transactions
- ?? Fine calculation for overdue books
- ?? Reporting and analytics

The project showcases advanced SQL skills including stored procedures, views, transaction management, and error handling.

---

## Features

Core Features
- **Book Management**: Add, search, and track book inventory
- **Member Management**: Register and manage library members
- **Borrowing System**: Borrow and return books with automatic validation
- **Fine Calculation**: Automatic fine calculation for overdue books ($0.50/day)
- **Search Functionality**: Search books by title, author, or genre
- **Borrowing History**: View complete borrowing history for any member

Advanced Features
- **Transaction Management**: Safe borrow/return operations with rollback
- **Error Handling**: Comprehensive validation with user-friendly messages
- **Reporting**: Multiple views for library analytics
- **Data Integrity**: Foreign keys, constraints, and check constraints

---

## Database Schema

Tables

1. Books Table
| Column | Type | Description |
|--------|------|-------------|
| book_id | INT (PK, Identity) | Unique book identifier |
| title | NVARCHAR(200) | Book title |
| author | NVARCHAR(100) | Book author |
| isbn | NVARCHAR(20) | ISBN number (unique) |
| genre | NVARCHAR(50) | Book genre |
| total_copies | INT | Total copies owned |
| available_copies | INT | Currently available copies |
| created_at | DATETIME | Record creation timestamp |

2. Members Table
| Column | Type | Description |
|--------|------|-------------|
| member_id | INT (PK, Identity) | Unique member identifier |
| first_name | NVARCHAR(50) | Member's first name |
| last_name | NVARCHAR(50) | Member's last name |
| email | NVARCHAR(100) | Email address (unique) |
| phone | NVARCHAR(20) | Phone number |
| membership_date | DATE | Date of membership |
| status | NVARCHAR(20) | Active/Inactive |

3. Borrowing Table
| Column | Type | Description |
|--------|------|-------------|
| borrow_id | INT (PK, Identity) | Transaction identifier |
| book_id | INT (FK) | Book being borrowed |
| member_id | INT (FK) | Member borrowing the book |
| borrow_date | DATE | Date of borrowing |
| due_date | DATE | Expected return date |
| return_date | DATE | Actual return date (NULL if not returned) |
| status | NVARCHAR(20) | Borrowed/Returned |
| fine_amount | DECIMAL(10,2) | Calculated fine amount |


## Project Structure

LibraryManagementSystem/
├── 01_CreateDatabase.sql      - Database creation
├── 02_CreateTables.sql        - Table creation with constraints
├── 03_InsertSampleData.sql    - Sample data
├── 04_CreateProcedures.sql    - Stored procedures
├── 05_CreateViews.sql         - Reporting views
├── 06_TestQueries.sql         - Complete test suite
└── README.md                  - This file

## Author

Rechael Lopes
GitHub: https://github.com/RechaelLop/LibraryManagementSystem 
