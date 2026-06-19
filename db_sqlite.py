import sqlite3
import os

def init_db():
    """Create SQLite database with sample data"""
    db_path = os.path.join(os.path.dirname(__file__), 'library.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT UNIQUE,
            genre TEXT,
            total_copies INTEGER DEFAULT 1,
            available_copies INTEGER DEFAULT 1
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS members (
            member_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            membership_date DATE DEFAULT CURRENT_DATE,
            status TEXT DEFAULT 'Active'
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS borrowing (
            borrow_id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            member_id INTEGER NOT NULL,
            borrow_date DATE NOT NULL,
            due_date DATE NOT NULL,
            return_date DATE,
            status TEXT DEFAULT 'Borrowed',
            fine_amount REAL DEFAULT 0
        )
    ''')
    
    # Insert sample data
    cursor.execute('SELECT COUNT(*) FROM books')
    if cursor.fetchone()[0] == 0:
        cursor.executemany('''
            INSERT INTO books (title, author, isbn, genre, total_copies, available_copies)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', [
            ('The Great Gatsby', 'F. Scott Fitzgerald', '978-0-7432-7356-5', 'Fiction', 3, 3),
            ('To Kill a Mockingbird', 'Harper Lee', '978-0-06-112008-4', 'Fiction', 2, 2),
            ('1984', 'George Orwell', '978-0-452-28423-4', 'Science Fiction', 4, 4),
            ('The Hobbit', 'J.R.R. Tolkien', '978-0-547-92822-7', 'Fantasy', 3, 3),
            ('Harry Potter', 'J.K. Rowling', '978-0-439-70818-8', 'Fantasy', 5, 5)
        ])
    
    conn.commit()
    conn.close()
    print("✅ SQLite database initialized!")

def get_connection():
    """Get SQLite connection"""
    db_path = os.path.join(os.path.dirname(__file__), 'library.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database if needed
if not os.path.exists(os.path.join(os.path.dirname(__file__), 'library.db')):
    init_db()