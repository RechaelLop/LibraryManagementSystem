# ============================================
# LIBRARY MANAGEMENT SYSTEM - FLASK WEB APP
# Supports both SQL Server (local) and SQLite (Railway)
# ============================================

from flask import Flask, render_template, request, jsonify
import os
import sys
from datetime import datetime, timedelta

app = Flask(__name__)

# ============================================
# DATABASE CONNECTION (Auto-detect environment)
# ============================================

def get_connection():
    """
    Automatically uses SQLite on Railway, SQL Server locally
    """
    # Check if running on Railway
    is_railway = os.environ.get('RAILWAY_ENVIRONMENT') is not None
    
    if is_railway:
        # Use SQLite on Railway
        import sqlite3
        db_path = os.path.join(os.path.dirname(__file__), 'library.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    else:
        # Use SQL Server locally
        try:
            import pyodbc
            conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=localhost;'
                'DATABASE=LibraryManagement;'
                'Trusted_Connection=yes;'
            )
            return conn
        except Exception as e:
            print(f"SQL Server connection error: {e}")
            # Fallback to SQLite
            import sqlite3
            db_path = os.path.join(os.path.dirname(__file__), 'library.db')
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            return conn

# ============================================
# INITIALIZE SQLITE DATABASE (for Railway)
# ============================================

def init_sqlite_db():
    """Create SQLite database with sample data for Railway"""
    db_path = os.path.join(os.path.dirname(__file__), 'library.db')
    
    # Skip if database already exists
    if os.path.exists(db_path):
        return
    
    import sqlite3
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create books table
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
    
    # Create members table
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
    
    # Create borrowing table
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
    
    # Insert sample books
    cursor.executemany('''
        INSERT OR IGNORE INTO books (title, author, isbn, genre, total_copies, available_copies)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', [
        ('The Great Gatsby', 'F. Scott Fitzgerald', '978-0-7432-7356-5', 'Fiction', 3, 3),
        ('To Kill a Mockingbird', 'Harper Lee', '978-0-06-112008-4', 'Fiction', 2, 2),
        ('1984', 'George Orwell', '978-0-452-28423-4', 'Science Fiction', 4, 4),
        ('The Hobbit', 'J.R.R. Tolkien', '978-0-547-92822-7', 'Fantasy', 3, 3),
        ('Harry Potter', 'J.K. Rowling', '978-0-439-70818-8', 'Fantasy', 5, 5),
        ('The Alchemist', 'Paulo Coelho', '978-0-06-250217-4', 'Fiction', 2, 2),
        ('Pride and Prejudice', 'Jane Austen', '978-0-14-143951-8', 'Romance', 2, 2),
        ('The Catcher in the Rye', 'J.D. Salinger', '978-0-316-76948-0', 'Fiction', 2, 2)
    ])
    
    # Insert sample members
    cursor.executemany('''
        INSERT OR IGNORE INTO members (first_name, last_name, email, phone, status)
        VALUES (?, ?, ?, ?, ?)
    ''', [
        ('John', 'Doe', 'john@email.com', '555-0101', 'Active'),
        ('Jane', 'Smith', 'jane@email.com', '555-0102', 'Active'),
        ('Robert', 'Johnson', 'robert@email.com', '555-0103', 'Active'),
        ('Emily', 'Brown', 'emily@email.com', '555-0104', 'Active'),
        ('Michael', 'Davis', 'michael@email.com', '555-0105', 'Active'),
        ('Sarah', 'Wilson', 'sarah@email.com', '555-0106', 'Inactive')
    ])
    
    conn.commit()
    conn.close()
    print("✅ SQLite database initialized with sample data!")

# Initialize SQLite database if needed
if os.environ.get('RAILWAY_ENVIRONMENT') is not None:
    init_sqlite_db()

# ============================================
# PAGE ROUTES
# ============================================

@app.route('/')
def dashboard_page():
    """Home page - Dashboard"""
    conn = get_connection()
    stats = {}
    
    if conn:
        try:
            cursor = conn.cursor()
            # Check if we're using SQLite or SQL Server
            is_sqlite = os.environ.get('RAILWAY_ENVIRONMENT') is not None
            
            if is_sqlite:
                # SQLite version - get stats manually
                cursor.execute("SELECT COUNT(*) FROM books")
                stats['total_books'] = cursor.fetchone()[0]
                
                cursor.execute("SELECT SUM(total_copies) FROM books")
                stats['total_copies'] = cursor.fetchone()[0] or 0
                
                cursor.execute("SELECT SUM(available_copies) FROM books")
                stats['available'] = cursor.fetchone()[0] or 0
                
                cursor.execute("SELECT COUNT(*) FROM members")
                stats['total_members'] = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM members WHERE status = 'Active'")
                stats['active_members'] = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM borrowing WHERE status = 'Borrowed'")
                stats['currently_borrowed'] = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM borrowing WHERE status = 'Borrowed' AND due_date < date('now')")
                stats['overdue'] = cursor.fetchone()[0]
                
                cursor.execute("SELECT SUM(fine_amount) FROM borrowing")
                stats['total_fines'] = cursor.fetchone()[0] or 0
                
                cursor.execute("SELECT COUNT(*) FROM borrowing")
                stats['total_transactions'] = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM borrowing WHERE status = 'Returned'")
                stats['completed_returns'] = cursor.fetchone()[0]
            else:
                # SQL Server version
                cursor.execute("SELECT * FROM LibraryStats")
                row = cursor.fetchone()
                if row:
                    stats = {
                        'total_books': row[0],
                        'total_copies': row[1],
                        'available': row[2],
                        'total_members': row[3],
                        'active_members': row[4],
                        'currently_borrowed': row[5],
                        'overdue': row[6],
                        'total_fines': row[7],
                        'total_transactions': row[8],
                        'completed_returns': row[9]
                    }
        except Exception as e:
            print(f"Dashboard error: {e}")
        finally:
            conn.close()
    
    return render_template('dashboard.html', stats=stats, active='dashboard')

@app.route('/books')
def books_page():
    return render_template('books.html', active='books')

@app.route('/members')
def members_page():
    return render_template('members.html', active='members')

@app.route('/borrow')
def borrow_page():
    return render_template('borrow.html', active='borrow')

@app.route('/return')
def return_page():
    return render_template('return.html', active='return')

@app.route('/search')
def search_page():
    return render_template('search.html', active='search')

# ============================================
# API ENDPOINTS
# ============================================

@app.route('/api/books')
def api_get_books():
    conn = get_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'})
    
    cursor = conn.cursor()
    is_sqlite = os.environ.get('RAILWAY_ENVIRONMENT') is not None
    
    if is_sqlite:
        cursor.execute("SELECT book_id, title, author, genre, available_copies, total_copies FROM books ORDER BY title")
    else:
        cursor.execute("SELECT book_id, title, author, genre, available_copies, total_copies FROM books ORDER BY title")
    
    rows = cursor.fetchall()
    conn.close()
    
    books = []
    for row in rows:
        if is_sqlite:
            books.append({
                'id': row[0],
                'title': row[1],
                'author': row[2],
                'genre': row[3] or 'N/A',
                'available': row[4],
                'total': row[5]
            })
        else:
            books.append({
                'id': row[0],
                'title': row[1],
                'author': row[2],
                'genre': row[3] or 'N/A',
                'available': row[4],
                'total': row[5]
            })
    
    return jsonify(books)

@app.route('/api/members')
def api_get_members():
    conn = get_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'})
    
    cursor = conn.cursor()
    is_sqlite = os.environ.get('RAILWAY_ENVIRONMENT') is not None
    
    if is_sqlite:
        cursor.execute("SELECT member_id, first_name, last_name, email, phone, status FROM members ORDER BY member_id")
    else:
        cursor.execute("SELECT member_id, CONCAT(first_name, ' ', last_name), email, phone, status FROM members ORDER BY member_id")
    
    rows = cursor.fetchall()
    conn.close()
    
    members = []
    for row in rows:
        if is_sqlite:
            members.append({
                'id': row[0],
                'name': f"{row[1]} {row[2]}",
                'email': row[3],
                'phone': row[4] or 'N/A',
                'status': row[5]
            })
        else:
            members.append({
                'id': row[0],
                'name': row[1],
                'email': row[2],
                'phone': row[3] or 'N/A',
                'status': row[4]
            })
    
    return jsonify(members)

@app.route('/api/borrow', methods=['POST'])
def api_borrow_book():
    member_id = request.form.get('member_id')
    book_id = request.form.get('book_id')
    days = int(request.form.get('days', 14))
    is_sqlite = os.environ.get('RAILWAY_ENVIRONMENT') is not None
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        if is_sqlite:
            # SQLite version
            cursor.execute("SELECT available_copies FROM books WHERE book_id = ?", (book_id,))
            row = cursor.fetchone()
            if not row or row[0] < 1:
                conn.close()
                return jsonify({'success': False, 'message': 'No copies available'})
            
            cursor.execute("SELECT status FROM members WHERE member_id = ?", (member_id,))
            member = cursor.fetchone()
            if not member or member[0] != 'Active':
                conn.close()
                return jsonify({'success': False, 'message': 'Member not active'})
            
            due_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
            cursor.execute('''
                INSERT INTO borrowing (book_id, member_id, borrow_date, due_date, status)
                VALUES (?, ?, date('now'), ?, 'Borrowed')
            ''', (book_id, member_id, due_date))
            
            cursor.execute("UPDATE books SET available_copies = available_copies - 1 WHERE book_id = ?", (book_id,))
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': f'✅ Book borrowed! Due: {due_date}'})
        else:
            # SQL Server version
            cursor.execute("EXEC BorrowBook ?, ?, ?", (member_id, book_id, days))
            result = cursor.fetchone()
            conn.commit()
            conn.close()
            if result and 'ERROR' not in result[0]:
                return jsonify({'success': True, 'message': result[0]})
            else:
                return jsonify({'success': False, 'message': result[0] if result else 'Failed to borrow book'})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/return', methods=['POST'])
def api_return_book():
    borrow_id = request.form.get('borrow_id')
    is_sqlite = os.environ.get('RAILWAY_ENVIRONMENT') is not None
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        if is_sqlite:
            # SQLite version
            cursor.execute("SELECT book_id, due_date FROM borrowing WHERE borrow_id = ? AND status = 'Borrowed'", (borrow_id,))
            row = cursor.fetchone()
            if not row:
                conn.close()
                return jsonify({'success': False, 'message': 'Invalid borrow ID or already returned'})
            
            due_date = datetime.strptime(row[1], '%Y-%m-%d')
            days_overdue = (datetime.now() - due_date).days
            fine = days_overdue * 0.50 if days_overdue > 0 else 0
            
            cursor.execute('''
                UPDATE borrowing 
                SET return_date = date('now'), status = 'Returned', fine_amount = ?
                WHERE borrow_id = ?
            ''', (fine, borrow_id))
            
            cursor.execute("UPDATE books SET available_copies = available_copies + 1 WHERE book_id = ?", (row[0],))
            conn.commit()
            conn.close()
            
            if fine > 0:
                return jsonify({'success': True, 'message': f'✅ Book returned! Fine: ${fine:.2f}'})
            else:
                return jsonify({'success': True, 'message': '✅ Book returned successfully!'})
        else:
            # SQL Server version
            cursor.execute("EXEC ReturnBook ?", (borrow_id,))
            result = cursor.fetchone()
            conn.commit()
            conn.close()
            if result and 'ERROR' not in result[0]:
                return jsonify({'success': True, 'message': result[0]})
            else:
                return jsonify({'success': False, 'message': result[0] if result else 'Failed to return book'})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/search')
def api_search_books():
    term = request.args.get('q', '')
    genre = request.args.get('genre', 'All')
    available_only = request.args.get('available', 'false') == 'true'
    is_sqlite = os.environ.get('RAILWAY_ENVIRONMENT') is not None
    
    if not term:
        return jsonify([])
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        if is_sqlite:
            # SQLite version
            query = """
                SELECT book_id, title, author, genre, available_copies, total_copies 
                FROM books 
                WHERE title LIKE ? OR author LIKE ?
            """
            params = [f'%{term}%', f'%{term}%']
            
            if genre != 'All':
                query += " AND genre = ?"
                params.append(genre)
            
            if available_only:
                query += " AND available_copies > 0"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            conn.close()
            
            results = []
            for row in rows:
                results.append({
                    'id': row[0],
                    'title': row[1],
                    'author': row[2],
                    'genre': row[3] or 'N/A',
                    'available': row[4],
                    'total': row[5]
                })
            return jsonify(results)
        else:
            # SQL Server version
            if genre == 'All':
                cursor.execute("EXEC SearchBooks ?, NULL, ?", (term, 1 if available_only else 0))
            else:
                cursor.execute("EXEC SearchBooks ?, ?, ?", (term, genre, 1 if available_only else 0))
            
            rows = cursor.fetchall()
            conn.close()
            
            results = []
            for row in rows:
                results.append({
                    'id': row[0],
                    'title': row[1],
                    'author': row[2],
                    'genre': row[4] or 'N/A',
                    'available': row[6],
                    'total': row[5]
                })
            return jsonify(results)
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)})

@app.route('/api/overdue')
def api_get_overdue():
    is_sqlite = os.environ.get('RAILWAY_ENVIRONMENT') is not None
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        if is_sqlite:
            # SQLite version
            cursor.execute('''
                SELECT b.borrow_id, bk.title, m.first_name || ' ' || m.last_name as member,
                       julianday('now') - julianday(b.due_date) as days_overdue,
                       (julianday('now') - julianday(b.due_date)) * 0.50 as fine
                FROM borrowing b
                JOIN books bk ON b.book_id = bk.book_id
                JOIN members m ON b.member_id = m.member_id
                WHERE b.status = 'Borrowed' AND b.due_date < date('now')
                ORDER BY b.due_date
            ''')
            rows = cursor.fetchall()
            conn.close()
            
            books = []
            for row in rows:
                books.append({
                    'id': row[0],
                    'book': row[1],
                    'member': row[2],
                    'days': int(row[3]),
                    'fine': round(row[4] if row[4] else 0, 2)
                })
            return jsonify(books)
        else:
            # SQL Server version
            cursor.execute("""
                SELECT borrow_id, BookTitle, MemberName, DaysOverdue, EstimatedFine
                FROM OverdueBooks
                ORDER BY DaysOverdue DESC
            """)
            rows = cursor.fetchall()
            conn.close()
            
            books = []
            for row in rows:
                books.append({
                    'id': row[0],
                    'book': row[1],
                    'member': row[2],
                    'days': row[3],
                    'fine': float(row[4]) if row[4] else 0
                })
            return jsonify(books)
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)})

@app.route('/api/borrowings')
def api_get_borrowings():
    is_sqlite = os.environ.get('RAILWAY_ENVIRONMENT') is not None
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        if is_sqlite:
            # SQLite version
            cursor.execute('''
                SELECT 
                    b.borrow_id, 
                    bk.title, 
                    m.first_name || ' ' || m.last_name as member_name,
                    b.due_date,
                    CASE 
                        WHEN b.due_date < date('now') THEN '⚠️ OVERDUE'
                        WHEN b.due_date <= date('now', '+3 days') THEN '🔴 Due Soon'
                        ELSE '✅ Active'
                    END as status
                FROM borrowing b
                JOIN books bk ON b.book_id = bk.book_id
                JOIN members m ON b.member_id = m.member_id
                WHERE b.status = 'Borrowed'
                ORDER BY b.due_date ASC
            ''')
            rows = cursor.fetchall()
            conn.close()
            
            borrowings = []
            for row in rows:
                borrowings.append({
                    'id': row[0],
                    'book': row[1],
                    'member': row[2],
                    'due_date': row[3],
                    'status': row[4]
                })
            return jsonify(borrowings)
        else:
            # SQL Server version
            cursor.execute("""
                SELECT 
                    b.borrow_id, 
                    bk.title, 
                    CONCAT(m.first_name, ' ', m.last_name) AS member_name,
                    b.due_date, 
                    CASE 
                        WHEN b.due_date < GETDATE() THEN '⚠️ OVERDUE'
                        WHEN b.due_date <= DATEADD(DAY, 3, GETDATE()) THEN '🔴 Due Soon'
                        ELSE '✅ Active'
                    END AS status
                FROM borrowing b
                JOIN books bk ON b.book_id = bk.book_id
                JOIN members m ON b.member_id = m.member_id
                WHERE b.status = 'Borrowed'
                ORDER BY b.due_date ASC
            """)
            rows = cursor.fetchall()
            conn.close()
            
            borrowings = []
            for row in rows:
                borrowings.append({
                    'id': row[0],
                    'book': row[1],
                    'member': row[2],
                    'due_date': row[3].strftime('%Y-%m-%d') if row[3] else 'N/A',
                    'status': row[4]
                })
            return jsonify(borrowings)
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)})

@app.route('/api/stats')
def api_get_stats():
    is_sqlite = os.environ.get('RAILWAY_ENVIRONMENT') is not None
    conn = get_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'})
    
    cursor = conn.cursor()
    stats = {}
    
    try:
        if is_sqlite:
            cursor.execute("SELECT COUNT(*) FROM books")
            stats['total_books'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT SUM(total_copies) FROM books")
            stats['total_copies'] = cursor.fetchone()[0] or 0
            
            cursor.execute("SELECT SUM(available_copies) FROM books")
            stats['available'] = cursor.fetchone()[0] or 0
            
            cursor.execute("SELECT COUNT(*) FROM members")
            stats['total_members'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM members WHERE status = 'Active'")
            stats['active_members'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM borrowing WHERE status = 'Borrowed'")
            stats['currently_borrowed'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM borrowing WHERE status = 'Borrowed' AND due_date < date('now')")
            stats['overdue'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT SUM(fine_amount) FROM borrowing")
            stats['total_fines'] = cursor.fetchone()[0] or 0
            
            cursor.execute("SELECT COUNT(*) FROM borrowing")
            stats['total_transactions'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM borrowing WHERE status = 'Returned'")
            stats['completed_returns'] = cursor.fetchone()[0]
        else:
            cursor.execute("SELECT * FROM LibraryStats")
            row = cursor.fetchone()
            if row:
                stats = {
                    'total_books': row[0],
                    'total_copies': row[1],
                    'available': row[2],
                    'total_members': row[3],
                    'active_members': row[4],
                    'currently_borrowed': row[5],
                    'overdue': row[6],
                    'total_fines': float(row[7]) if row[7] else 0,
                    'total_transactions': row[8],
                    'completed_returns': row[9]
                }
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)})
    
    conn.close()
    return jsonify(stats)

# ============================================
# RUN THE APP
# ============================================

if __name__ == '__main__':
    print("=" * 50)
    print("📚 Library Management System - Web App")
    print("=" * 50)
    
    is_railway = os.environ.get('RAILWAY_ENVIRONMENT') is not None
    if is_railway:
        print("🌐 Running on Railway (SQLite mode)")
    else:
        print("💻 Running locally (SQL Server mode)")
    
    print(f"🚀 Server running at: http://localhost:5000")
    print(f"📊 Dashboard: http://localhost:5000")
    print("=" * 50)
    print("Press CTRL+C to stop the server")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)