# ============================================
# LIBRARY MANAGEMENT SYSTEM - MODERN UI
# Clean, Simple, and User-Friendly
# ============================================

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, font
import pyodbc
from datetime import datetime

# ============================================
# COLORS AND STYLES
# ============================================

COLORS = {
    'bg': '#f0f4f8',
    'primary': '#2c3e50',
    'secondary': '#3498db',
    'success': '#27ae60',
    'danger': '#e74c3c',
    'warning': '#f39c12',
    'card': '#ffffff',
    'text': '#2c3e50',
    'light': '#ecf0f1'
}

# ============================================
# DATABASE CONNECTION
# ============================================

def get_connection():
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=localhost;'
            'DATABASE=LibraryManagement;'
            'Trusted_Connection=yes;'
        )
        return conn
    except Exception as e:
        return None

# ============================================
# MAIN APPLICATION
# ============================================

class ModernLibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📚 Library Management System")
        self.root.geometry("1100x700")
        self.root.configure(bg=COLORS['bg'])
        
        # Configure styles
        self.setup_styles()
        
        # Create header
        self.create_header()
        
        # Create main content area with sidebar
        self.create_main_layout()
        
        # Show default page
        self.show_dashboard()
        
        # Status bar
        self.create_status_bar()
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button style
        style.configure('Primary.TButton', 
                       background=COLORS['secondary'],
                       foreground='white',
                       font=('Segoe UI', 10))
        
        style.configure('Success.TButton',
                       background=COLORS['success'],
                       foreground='white',
                       font=('Segoe UI', 10))
        
        style.configure('Danger.TButton',
                       background=COLORS['danger'],
                       foreground='white',
                       font=('Segoe UI', 10))
        
        # Configure Treeview
        style.configure('Treeview', 
                       font=('Segoe UI', 10),
                       rowheight=30)
        style.configure('Treeview.Heading', 
                       font=('Segoe UI', 10, 'bold'),
                       background=COLORS['primary'],
                       foreground='white')
    
    def create_header(self):
        header = tk.Frame(self.root, bg=COLORS['primary'], height=70)
        header.pack(fill='x', side='top')
        header.pack_propagate(False)
        
        # Title
        title = tk.Label(header, 
                        text="📚 Library Management System",
                        font=('Segoe UI', 20, 'bold'),
                        bg=COLORS['primary'],
                        fg='white')
        title.pack(side='left', padx=30, pady=15)
        
        # Date/Time
        self.time_label = tk.Label(header,
                                   font=('Segoe UI', 10),
                                   bg=COLORS['primary'],
                                   fg='white')
        self.time_label.pack(side='right', padx=30)
        self.update_time()
    
    def update_time(self):
        now = datetime.now().strftime("%A, %B %d, %Y  %I:%M %p")
        self.time_label.config(text=now)
        self.root.after(60000, self.update_time)
    
    def create_main_layout(self):
        main_container = tk.Frame(self.root, bg=COLORS['bg'])
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Sidebar
        sidebar = tk.Frame(main_container, bg=COLORS['card'], width=200, relief='raised', bd=1)
        sidebar.pack(side='left', fill='y', padx=(0, 20))
        sidebar.pack_propagate(False)
        
        # Sidebar buttons
        buttons = [
            ("📊 Dashboard", self.show_dashboard),
            ("📖 Books", self.show_books),
            ("👤 Members", self.show_members),
            ("📤 Borrow", self.show_borrow),
            ("📥 Return", self.show_return),
            ("🔍 Search", self.show_search),
            ("⚠️ Overdue", self.show_overdue)
        ]
        
        for text, command in buttons:
            btn = tk.Button(sidebar,
                           text=text,
                           command=command,
                           font=('Segoe UI', 11),
                           bg=COLORS['card'],
                           fg=COLORS['text'],
                           relief='flat',
                           anchor='w',
                           padx=20,
                           pady=12,
                           width=20)
            btn.pack(fill='x')
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg=COLORS['light']))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg=COLORS['card']))
        
        # Content area
        self.content = tk.Frame(main_container, bg=COLORS['card'], relief='flat')
        self.content.pack(side='left', fill='both', expand=True)
    
    def create_status_bar(self):
        status = tk.Frame(self.root, bg=COLORS['light'], height=30)
        status.pack(fill='x', side='bottom')
        status.pack_propagate(False)
        
        self.status_label = tk.Label(status,
                                     text="Ready",
                                     font=('Segoe UI', 9),
                                     bg=COLORS['light'],
                                     fg=COLORS['text'])
        self.status_label.pack(side='left', padx=15, pady=5)
    
    def set_status(self, message):
        self.status_label.config(text=message)
        self.root.update()
    
    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()
    
    # ============================================
    # DASHBOARD
    # ============================================
    
    def show_dashboard(self):
        self.clear_content()
        
        # Header
        header = tk.Label(self.content,
                         text="📊 Dashboard",
                         font=('Segoe UI', 18, 'bold'),
                         bg=COLORS['card'],
                         fg=COLORS['primary'])
        header.pack(pady=(20, 10), padx=30, anchor='w')
        
        # Stats cards
        stats_frame = tk.Frame(self.content, bg=COLORS['card'])
        stats_frame.pack(fill='x', padx=30, pady=20)
        
        # Get stats
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM LibraryStats")
            stats = cursor.fetchone()
            conn.close()
            
            if stats:
                cards = [
                    ("Total Books", stats[0]),
                    ("Available", stats[2]),
                    ("Members", stats[3]),
                    ("Active Members", stats[4]),
                    ("Currently Borrowed", stats[5]),
                    ("Overdue", stats[6])
                ]
                
                for i, (label, value) in enumerate(cards):
                    card = tk.Frame(stats_frame, bg=COLORS['light'], relief='flat', bd=1)
                    card.grid(row=i//3, column=i%3, padx=10, pady=10, sticky='nsew')
                    
                    tk.Label(card,
                            text=str(value),
                            font=('Segoe UI', 24, 'bold'),
                            bg=COLORS['light'],
                            fg=COLORS['primary']).pack(pady=(15, 5))
                    
                    tk.Label(card,
                            text=label,
                            font=('Segoe UI', 10),
                            bg=COLORS['light'],
                            fg=COLORS['text']).pack(pady=(0, 15))
                    
                    stats_frame.grid_columnconfigure(i%3, weight=1)
        else:
            tk.Label(self.content,
                    text="❌ Could not load dashboard",
                    font=('Segoe UI', 14),
                    bg=COLORS['card'],
                    fg=COLORS['danger']).pack(pady=50)
        
        # Recent activity
        tk.Label(self.content,
                text="📋 Recent Borrowings",
                font=('Segoe UI', 14, 'bold'),
                bg=COLORS['card'],
                fg=COLORS['primary']).pack(anchor='w', padx=30, pady=(20, 10))
        
        self.show_recent_borrowings()
    
    def show_recent_borrowings(self):
        tree = ttk.Treeview(self.content, columns=('Book', 'Member', 'Date', 'Status'), show='headings', height=6)
        tree.heading('Book', text='Book')
        tree.heading('Member', text='Member')
        tree.heading('Date', text='Borrow Date')
        tree.heading('Status', text='Status')
        tree.column('Book', width=250)
        tree.column('Member', width=200)
        tree.column('Date', width=120)
        tree.column('Status', width=100)
        
        tree.pack(fill='x', padx=30, pady=(0, 20))
        
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT TOP 10 bk.title, CONCAT(m.first_name, ' ', m.last_name), 
                       b.borrow_date, b.status
                FROM borrowing b
                JOIN books bk ON b.book_id = bk.book_id
                JOIN members m ON b.member_id = m.member_id
                ORDER BY b.borrow_date DESC
            """)
            rows = cursor.fetchall()
            conn.close()
            
            for row in rows:
                tree.insert('', 'end', values=row)
    
    # ============================================
    # BOOKS PAGE
    # ============================================
    
    def show_books(self):
        self.clear_content()
        
        # Header
        tk.Label(self.content,
                text="📖 Books",
                font=('Segoe UI', 18, 'bold'),
                bg=COLORS['card'],
                fg=COLORS['primary']).pack(pady=(20, 10), padx=30, anchor='w')
        
        # Controls
        controls = tk.Frame(self.content, bg=COLORS['card'])
        controls.pack(fill='x', padx=30, pady=10)
        
        tk.Label(controls, text="Search:", font=('Segoe UI', 10), bg=COLORS['card']).pack(side='left', padx=5)
        self.book_search_var = tk.StringVar()
        search_entry = tk.Entry(controls, textvariable=self.book_search_var, width=30, font=('Segoe UI', 10))
        search_entry.pack(side='left', padx=5)
        
        tk.Button(controls, text="🔍", command=self.search_books, 
                 font=('Segoe UI', 10), bg=COLORS['secondary'], fg='white', padx=15, pady=5).pack(side='left', padx=5)
        tk.Button(controls, text="🔄 Refresh", command=self.refresh_books,
                 font=('Segoe UI', 10), bg=COLORS['light'], fg=COLORS['text'], padx=15, pady=5).pack(side='left', padx=5)
        tk.Button(controls, text="➕ Add Book", command=self.add_book,
                 font=('Segoe UI', 10), bg=COLORS['success'], fg='white', padx=15, pady=5).pack(side='left', padx=5)
        
        # Books table
        self.create_books_table()
        self.refresh_books()
    
    def create_books_table(self):
        # Treeview frame with scrollbar
        tree_frame = tk.Frame(self.content, bg=COLORS['card'])
        tree_frame.pack(fill='both', expand=True, padx=30, pady=10)
        
        self.books_tree = ttk.Treeview(tree_frame, 
                                       columns=('ID', 'Title', 'Author', 'Genre', 'Available', 'Total'), 
                                       show='headings')
        self.books_tree.heading('ID', text='ID')
        self.books_tree.heading('Title', text='Title')
        self.books_tree.heading('Author', text='Author')
        self.books_tree.heading('Genre', text='Genre')
        self.books_tree.heading('Available', text='Available')
        self.books_tree.heading('Total', text='Total')
        self.books_tree.column('ID', width=50)
        self.books_tree.column('Title', width=300)
        self.books_tree.column('Author', width=200)
        self.books_tree.column('Genre', width=150)
        self.books_tree.column('Available', width=100)
        self.books_tree.column('Total', width=100)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.books_tree.yview)
        self.books_tree.configure(yscrollcommand=scrollbar.set)
        
        self.books_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def refresh_books(self):
        self.book_search_var.set("")
        self.load_books()
    
    def search_books(self):
        self.load_books()
    
    def load_books(self):
        search = self.book_search_var.get().strip()
        
        for item in self.books_tree.get_children():
            self.books_tree.delete(item)
        
        conn = get_connection()
        if not conn:
            return
        
        cursor = conn.cursor()
        if search:
            cursor.execute("""
                SELECT book_id, title, author, genre, available_copies, total_copies
                FROM books
                WHERE title LIKE ? OR author LIKE ?
                ORDER BY title
            """, (f'%{search}%', f'%{search}%'))
        else:
            cursor.execute("SELECT book_id, title, author, genre, available_copies, total_copies FROM books ORDER BY title")
        
        rows = cursor.fetchall()
        conn.close()
        
        for row in rows:
            self.books_tree.insert('', 'end', values=row)
        
        self.set_status(f"📚 {len(rows)} books loaded")
    
    def add_book(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Book")
        dialog.geometry("450x400")
        dialog.configure(bg=COLORS['card'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Add New Book", font=('Segoe UI', 16, 'bold'),
                bg=COLORS['card'], fg=COLORS['primary']).pack(pady=20)
        
        frame = tk.Frame(dialog, bg=COLORS['card'])
        frame.pack(padx=30, pady=10)
        
        fields = [
            ("Title:", tk.Entry, {}),
            ("Author:", tk.Entry, {}),
            ("ISBN:", tk.Entry, {}),
            ("Genre:", tk.Combobox, {'values': ('Fiction', 'Science Fiction', 'Fantasy', 'Romance', 'Mystery', 'Non-Fiction')}),
            ("Copies:", tk.Entry, {})
        ]
        
        entries = {}
        for i, (label, widget, kwargs) in enumerate(fields):
            tk.Label(frame, text=label, font=('Segoe UI', 10), bg=COLORS['card']).grid(row=i, column=0, sticky='e', padx=10, pady=8)
            entry = widget(frame, width=30, font=('Segoe UI', 10))
            if label == "Copies:":
                entry.insert(0, "1")
            entry.grid(row=i, column=1, padx=10, pady=8)
            entries[label.replace(":", "")] = entry
        
        def save():
            data = {k: v.get().strip() for k, v in entries.items()}
            if not data['Title'] or not data['Author']:
                messagebox.showwarning("Warning", "Title and Author are required")
                return
            
            try:
                copies = int(data['Copies'])
            except:
                copies = 1
            
            conn = get_connection()
            if not conn:
                return
            
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO books (title, author, isbn, genre, total_copies, available_copies)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (data['Title'], data['Author'], data['ISBN'], data['Genre'], copies, copies))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", f"Book '{data['Title']}' added!")
            dialog.destroy()
            self.load_books()
        
        tk.Button(dialog, text="💾 Save Book", command=save,
                 font=('Segoe UI', 11), bg=COLORS['success'], fg='white', padx=30, pady=10).pack(pady=20)
    
    # ============================================
    # MEMBERS PAGE
    # ============================================
    
    def show_members(self):
        self.clear_content()
        
        tk.Label(self.content,
                text="👤 Members",
                font=('Segoe UI', 18, 'bold'),
                bg=COLORS['card'],
                fg=COLORS['primary']).pack(pady=(20, 10), padx=30, anchor='w')
        
        # Controls
        controls = tk.Frame(self.content, bg=COLORS['card'])
        controls.pack(fill='x', padx=30, pady=10)
        
        tk.Button(controls, text="🔄 Refresh", command=self.refresh_members,
                 font=('Segoe UI', 10), bg=COLORS['light'], fg=COLORS['text'], padx=15, pady=5).pack(side='left', padx=5)
        tk.Button(controls, text="➕ Add Member", command=self.add_member,
                 font=('Segoe UI', 10), bg=COLORS['success'], fg='white', padx=15, pady=5).pack(side='left', padx=5)
        
        # Members table
        tree_frame = tk.Frame(self.content, bg=COLORS['card'])
        tree_frame.pack(fill='both', expand=True, padx=30, pady=10)
        
        self.members_tree = ttk.Treeview(tree_frame, 
                                         columns=('ID', 'Name', 'Email', 'Phone', 'Status'), 
                                         show='headings')
        self.members_tree.heading('ID', text='ID')
        self.members_tree.heading('Name', text='Name')
        self.members_tree.heading('Email', text='Email')
        self.members_tree.heading('Phone', text='Phone')
        self.members_tree.heading('Status', text='Status')
        self.members_tree.column('ID', width=50)
        self.members_tree.column('Name', width=200)
        self.members_tree.column('Email', width=250)
        self.members_tree.column('Phone', width=150)
        self.members_tree.column('Status', width=100)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.members_tree.yview)
        self.members_tree.configure(yscrollcommand=scrollbar.set)
        
        self.members_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.refresh_members()
    
    def refresh_members(self):
        for item in self.members_tree.get_children():
            self.members_tree.delete(item)
        
        conn = get_connection()
        if not conn:
            return
        
        cursor = conn.cursor()
        cursor.execute("SELECT member_id, CONCAT(first_name, ' ', last_name), email, phone, status FROM members ORDER BY member_id")
        rows = cursor.fetchall()
        conn.close()
        
        for row in rows:
            self.members_tree.insert('', 'end', values=row)
        
        self.set_status(f"👤 {len(rows)} members loaded")
    
    def add_member(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Member")
        dialog.geometry("450x400")
        dialog.configure(bg=COLORS['card'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Add New Member", font=('Segoe UI', 16, 'bold'),
                bg=COLORS['card'], fg=COLORS['primary']).pack(pady=20)
        
        frame = tk.Frame(dialog, bg=COLORS['card'])
        frame.pack(padx=30, pady=10)
        
        fields = [
            ("First Name:", tk.Entry, {}),
            ("Last Name:", tk.Entry, {}),
            ("Email:", tk.Entry, {}),
            ("Phone:", tk.Entry, {})
        ]
        
        entries = {}
        for i, (label, widget, kwargs) in enumerate(fields):
            tk.Label(frame, text=label, font=('Segoe UI', 10), bg=COLORS['card']).grid(row=i, column=0, sticky='e', padx=10, pady=8)
            entry = widget(frame, width=30, font=('Segoe UI', 10))
            entry.grid(row=i, column=1, padx=10, pady=8)
            entries[label.replace(":", "")] = entry
        
        def save():
            data = {k: v.get().strip() for k, v in entries.items()}
            if not data['First Name'] or not data['Last Name'] or not data['Email']:
                messagebox.showwarning("Warning", "Name and Email are required")
                return
            
            conn = get_connection()
            if not conn:
                return
            
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO members (first_name, last_name, email, phone, status)
                    VALUES (?, ?, ?, ?, 'Active')
                """, (data['First Name'], data['Last Name'], data['Email'], data['Phone']))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", f"Member '{data['First Name']} {data['Last Name']}' added!")
                dialog.destroy()
                self.refresh_members()
            except Exception as e:
                messagebox.showerror("Error", str(e))
                conn.close()
        
        tk.Button(dialog, text="💾 Save Member", command=save,
                 font=('Segoe UI', 11), bg=COLORS['success'], fg='white', padx=30, pady=10).pack(pady=20)
    
    # ============================================
    # BORROW PAGE
    # ============================================
    
    def show_borrow(self):
        self.clear_content()
        
        tk.Label(self.content,
                text="📤 Borrow a Book",
                font=('Segoe UI', 18, 'bold'),
                bg=COLORS['card'],
                fg=COLORS['primary']).pack(pady=(20, 10), padx=30, anchor='w')
        
        # Main form
        form_frame = tk.Frame(self.content, bg=COLORS['card'])
        form_frame.pack(padx=30, pady=10, fill='x')
        
        # Member ID
        tk.Label(form_frame, text="Member ID:", font=('Segoe UI', 11), bg=COLORS['card']).grid(row=0, column=0, sticky='e', padx=10, pady=10)
        self.borrow_member = tk.Entry(form_frame, width=20, font=('Segoe UI', 11))
        self.borrow_member.grid(row=0, column=1, padx=10, pady=10)
        tk.Button(form_frame, text="Check", command=self.check_member_borrow,
                 font=('Segoe UI', 10), bg=COLORS['secondary'], fg='white', padx=10).grid(row=0, column=2, padx=5)
        
        # Book ID
        tk.Label(form_frame, text="Book ID:", font=('Segoe UI', 11), bg=COLORS['card']).grid(row=1, column=0, sticky='e', padx=10, pady=10)
        self.borrow_book = tk.Entry(form_frame, width=20, font=('Segoe UI', 11))
        self.borrow_book.grid(row=1, column=1, padx=10, pady=10)
        tk.Button(form_frame, text="Check", command=self.check_book_borrow,
                 font=('Segoe UI', 10), bg=COLORS['secondary'], fg='white', padx=10).grid(row=1, column=2, padx=5)
        
        # Days
        tk.Label(form_frame, text="Days:", font=('Segoe UI', 11), bg=COLORS['card']).grid(row=2, column=0, sticky='e', padx=10, pady=10)
        self.borrow_days = tk.Entry(form_frame, width=20, font=('Segoe UI', 11))
        self.borrow_days.insert(0, "14")
        self.borrow_days.grid(row=2, column=1, padx=10, pady=10)
        
        # Info display
        self.borrow_info = scrolledtext.ScrolledText(form_frame, height=5, width=50, font=('Segoe UI', 10))
        self.borrow_info.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
        
        # Borrow button
        tk.Button(self.content, text="📤 Borrow Book", command=self.borrow_book,
                 font=('Segoe UI', 12), bg=COLORS['success'], fg='white', padx=40, pady=10).pack(pady=10)
    
    def check_member_borrow(self):
        member_id = self.borrow_member.get().strip()
        if not member_id:
            return
        
        conn = get_connection()
        if not conn:
            return
        
        cursor = conn.cursor()
        cursor.execute("SELECT CONCAT(first_name, ' ', last_name), status FROM members WHERE member_id = ?", (member_id,))
        row = cursor.fetchone()
        conn.close()
        
        self.borrow_info.delete('1.0', 'end')
        if row:
            self.borrow_info.insert('end', f"Member: {row[0]}\nStatus: {row[1]}")
        else:
            self.borrow_info.insert('end', "❌ Member not found")
    
    def check_book_borrow(self):
        book_id = self.borrow_book.get().strip()
        if not book_id:
            return
        
        conn = get_connection()
        if not conn:
            return
        
        cursor = conn.cursor()
        cursor.execute("SELECT title, available_copies FROM books WHERE book_id = ?", (book_id,))
        row = cursor.fetchone()
        conn.close()
        
        self.borrow_info.delete('1.0', 'end')
        if row:
            self.borrow_info.insert('end', f"Book: {row[0]}\nAvailable: {row[1]}")
        else:
            self.borrow_info.insert('end', "❌ Book not found")
    
    def borrow_book(self):
        member_id = self.borrow_member.get().strip()
        book_id = self.borrow_book.get().strip()
        days = self.borrow_days.get().strip()
        
        if not member_id or not book_id:
            messagebox.showwarning("Warning", "Please enter Member ID and Book ID")
            return
        
        try:
            days = int(days)
        except:
            days = 14
        
        conn = get_connection()
        if not conn:
            return
        
        cursor = conn.cursor()
        try:
            cursor.execute("EXEC BorrowBook ?, ?, ?", (member_id, book_id, days))
            result = cursor.fetchone()
            conn.commit()
            conn.close()
            
            if result:
                self.borrow_info.delete('1.0', 'end')
                self.borrow_info.insert('end', result[0])
                self.set_status("✅ Book borrowed successfully!")
            else:
                messagebox.showerror("Error", "Failed to borrow book")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            conn.close()
    
    # ============================================
    # RETURN PAGE
    # ============================================
    
    def show_return(self):
        self.clear_content()
        
        tk.Label(self.content,
                text="📥 Return a Book",
                font=('Segoe UI', 18, 'bold'),
                bg=COLORS['card'],
                fg=COLORS['primary']).pack(pady=(20, 10), padx=30, anchor='w')
        
        # Form
        form_frame = tk.Frame(self.content, bg=COLORS['card'])
        form_frame.pack(padx=30, pady=10, fill='x')
        
        tk.Label(form_frame, text="Borrow ID:", font=('Segoe UI', 11), bg=COLORS['card']).grid(row=0, column=0, sticky='e', padx=10, pady=10)
        self.return_id = tk.Entry(form_frame, width=20, font=('Segoe UI', 11))
        self.return_id.grid(row=0, column=1, padx=10, pady=10)
        tk.Button(form_frame, text="Check", command=self.check_return,
                 font=('Segoe UI', 10), bg=COLORS['secondary'], fg='white', padx=10).grid(row=0, column=2, padx=5)
        
        self.return_info = scrolledtext.ScrolledText(form_frame, height=5, width=50, font=('Segoe UI', 10))
        self.return_info.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        
        tk.Button(self.content, text="📥 Return Book", command=self.return_book,
                 font=('Segoe UI', 12), bg=COLORS['danger'], fg='white', padx=40, pady=10).pack(pady=10)
        
        # Overdue list
        tk.Label(self.content,
                text="⚠️ Overdue Books",
                font=('Segoe UI', 14, 'bold'),
                bg=COLORS['card'],
                fg=COLORS['danger']).pack(anchor='w', padx=30, pady=(20, 10))
        
        tree_frame = tk.Frame(self.content, bg=COLORS['card'])
        tree_frame.pack(fill='both', expand=True, padx=30, pady=10)
        
        self.overdue_tree = ttk.Treeview(tree_frame, 
                                         columns=('ID', 'Book', 'Member', 'Days'), 
                                         show='headings')
        self.overdue_tree.heading('ID', text='ID')
        self.overdue_tree.heading('Book', text='Book')
        self.overdue_tree.heading('Member', text='Member')
        self.overdue_tree.heading('Days', text='Days Overdue')
        self.overdue_tree.column('ID', width=50)
        self.overdue_tree.column('Book', width=250)
        self.overdue_tree.column('Member', width=200)
        self.overdue_tree.column('Days', width=100)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.overdue_tree.yview)
        self.overdue_tree.configure(yscrollcommand=scrollbar.set)
        
        self.overdue_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.refresh_overdue()
    
    def refresh_overdue(self):
        for item in self.overdue_tree.get_children():
            self.overdue_tree.delete(item)
        
        conn = get_connection()
        if not conn:
            return
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT borrow_id, BookTitle, MemberName, DaysOverdue
            FROM OverdueBooks
            ORDER BY DaysOverdue DESC
        """)
        rows = cursor.fetchall()
        conn.close()
        
        for row in rows:
            self.overdue_tree.insert('', 'end', values=row)
    
    def check_return(self):
        borrow_id = self.return_id.get().strip()
        if not borrow_id:
            return
        
        conn = get_connection()
        if not conn:
            return
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT bk.title, CONCAT(m.first_name, ' ', m.last_name), b.due_date, b.status
            FROM borrowing b
            JOIN books bk ON b.book_id = bk.book_id
            JOIN members m ON b.member_id = m.member_id
            WHERE b.borrow_id = ?
        """, (borrow_id,))
        row = cursor.fetchone()
        conn.close()
        
        self.return_info.delete('1.0', 'end')
        if row:
            self.return_info.insert('end', f"Book: {row[0]}\nMember: {row[1]}\nDue Date: {row[2]}\nStatus: {row[3]}")
        else:
            self.return_info.insert('end', "❌ Borrow record not found")
    
    def return_book(self):
        borrow_id = self.return_id.get().strip()
        if not borrow_id:
            messagebox.showwarning("Warning", "Please enter a Borrow ID")
            return
        
        conn = get_connection()
        if not conn:
            return
        
        cursor = conn.cursor()
        try:
            cursor.execute("EXEC ReturnBook ?", (borrow_id,))
            result = cursor.fetchone()
            conn.commit()
            conn.close()
            
            if result:
                self.return_info.delete('1.0', 'end')
                self.return_info.insert('end', result[0])
                self.set_status("✅ Book returned successfully!")
                self.refresh_overdue()
            else:
                messagebox.showerror("Error", "Failed to return book")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            conn.close()
    
    # ============================================
    # SEARCH PAGE
    # ============================================
    
    def show_search(self):
        self.clear_content()
        
        tk.Label(self.content,
                text="🔍 Search Books",
                font=('Segoe UI', 18, 'bold'),
                bg=COLORS['card'],
                fg=COLORS['primary']).pack(pady=(20, 10), padx=30, anchor='w')
        
        # Search form
        form_frame = tk.Frame(self.content, bg=COLORS['card'])
        form_frame.pack(padx=30, pady=10, fill='x')
        
        tk.Label(form_frame, text="Search:", font=('Segoe UI', 11), bg=COLORS['card']).grid(row=0, column=0, sticky='e', padx=10, pady=10)
        self.search_term = tk.Entry(form_frame, width=30, font=('Segoe UI', 11))
        self.search_term.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(form_frame, text="Genre:", font=('Segoe UI', 11), bg=COLORS['card']).grid(row=1, column=0, sticky='e', padx=10, pady=10)
        self.search_genre = ttk.Combobox(form_frame, values=('All', 'Fiction', 'Science Fiction', 'Fantasy', 'Romance', 'Mystery'), width=27)
        self.search_genre.current(0)
        self.search_genre.grid(row=1, column=1, padx=10, pady=10)
        
        self.search_available = tk.BooleanVar()
        tk.Checkbutton(form_frame, text="Only show available books", variable=self.search_available,
                      bg=COLORS['card'], font=('Segoe UI', 10)).grid(row=2, column=1, padx=10, pady=10)
        
        tk.Button(self.content, text="🔍 Search", command=self.perform_search,
                 font=('Segoe UI', 12), bg=COLORS['secondary'], fg='white', padx=40, pady=10).pack(pady=10)
        
        # Results
        self.search_results = scrolledtext.ScrolledText(self.content, height=15, font=('Segoe UI', 10))
        self.search_results.pack(fill='both', expand=True, padx=30, pady=10)
    
    def perform_search(self):
        term = self.search_term.get().strip()
        genre = self.search_genre.get()
        available = self.search_available.get()
        
        if not term:
            messagebox.showwarning("Warning", "Please enter a search term")
            return
        
        self.search_results.delete('1.0', 'end')
        
        conn = get_connection()
        if not conn:
            return
        
        cursor = conn.cursor()
        try:
            if genre == 'All':
                cursor.execute("EXEC SearchBooks ?, NULL, ?", (term, 1 if available else 0))
            else:
                cursor.execute("EXEC SearchBooks ?, ?, ?", (term, genre, 1 if available else 0))
            
            rows = cursor.fetchall()
            conn.close()
            
            if rows:
                self.search_results.insert('end', f"📚 Found {len(rows)} books:\n\n")
                for row in rows:
                    self.search_results.insert('end', f"📖 {row[1]} by {row[2]}\n")
                    self.search_results.insert('end', f"   Genre: {row[4]} | Available: {row[6]}/{row[5]}\n\n")
            else:
                self.search_results.insert('end', "❌ No books found matching your search.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            conn.close()
    
    # ============================================
    # OVERDUE PAGE
    # ============================================
    
    def show_overdue(self):
        self.clear_content()
        
        tk.Label(self.content,
                text="⚠️ Overdue Books",
                font=('Segoe UI', 18, 'bold'),
                bg=COLORS['card'],
                fg=COLORS['danger']).pack(pady=(20, 10), padx=30, anchor='w')
        
        # Overdue table
        tree_frame = tk.Frame(self.content, bg=COLORS['card'])
        tree_frame.pack(fill='both', expand=True, padx=30, pady=10)
        
        self.overdue_report = ttk.Treeview(tree_frame, 
                                           columns=('ID', 'Book', 'Member', 'Due Date', 'Days', 'Fine'), 
                                           show='headings')
        self.overdue_report.heading('ID', text='ID')
        self.overdue_report.heading('Book', text='Book')
        self.overdue_report.heading('Member', text='Member')
        self.overdue_report.heading('Due Date', text='Due Date')
        self.overdue_report.heading('Days', text='Days Overdue')
        self.overdue_report.heading('Fine', text='Fine')
        self.overdue_report.column('ID', width=50)
        self.overdue_report.column('Book', width=250)
        self.overdue_report.column('Member', width=200)
        self.overdue_report.column('Due Date', width=100)
        self.overdue_report.column('Days', width=100)
        self.overdue_report.column('Fine', width=100)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.overdue_report.yview)
        self.overdue_report.configure(yscrollcommand=scrollbar.set)
        
        self.overdue_report.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        tk.Button(self.content, text="🔄 Refresh", command=self.refresh_overdue_report,
                 font=('Segoe UI', 10), bg=COLORS['light'], fg=COLORS['text'], padx=20, pady=8).pack(pady=10)
        
        self.refresh_overdue_report()
    
    def refresh_overdue_report(self):
        for item in self.overdue_report.get_children():
            self.overdue_report.delete(item)
        
        conn = get_connection()
        if not conn:
            return
        
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM OverdueBooks ORDER BY DaysOverdue DESC")
        rows = cursor.fetchall()
        conn.close()
        
        for row in rows:
            self.overdue_report.insert('', 'end', values=row)
        
        self.set_status(f"⚠️ {len(rows)} overdue books found")

# ============================================
# RUN THE APPLICATION
# ============================================

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernLibraryApp(root)
    root.mainloop()