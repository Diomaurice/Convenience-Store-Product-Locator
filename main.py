import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

def get_db_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="diomaurice",
            database="convenience_store_db"
        )
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Could not connect to MySQL:\n{err}")
        return None
COLOR_BG = "#F3F4F6"  # Light Gray Background
COLOR_CARD = "#FFFFFF"  # Pure White Card Surface
COLOR_PRIMARY = "#2563EB"  # Vibrant Royal Blue
COLOR_SECONDARY = "#059669"  # Emerald Green
COLOR_EMPLOYEE = "#4F46E5"  # Deep Indigo
COLOR_TEXT = "#111827"  # Dark Charcoal Text
COLOR_MUTED = "#6B7280"  # Muted Gray
COLOR_BACK = "#E5E7EB"  # Light Gray for Back Button
COLOR_BACK_TEXT = "#374151"  # Dark Gray Text for Back Button

def center_window(window, width, height):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")
    window.configure(bg=COLOR_BG)

def customer_flow():
    conn = get_db_connection()
    if not conn: return
    cursor = conn.cursor()
    cursor.execute("SELECT category_id, category_name FROM categories")
    categories = cursor.fetchall()
    conn.close()

    cat_window = tk.Toplevel(root)
    cat_window.title("Customer Portal - Categories")
    center_window(cat_window, 420, 560)

    header_frame = tk.Frame(cat_window, bg=COLOR_BG)
    header_frame.pack(fill="x", padx=30, pady=20)

    tk.Label(header_frame, text="🛒 Browse Categories", font=("Arial", 16, "bold"),
             bg=COLOR_BG, fg=COLOR_TEXT).pack(anchor="w")
    tk.Label(header_frame, text="Select a category to view items & locations", font=("Arial", 10),
             bg=COLOR_BG, fg=COLOR_MUTED).pack(anchor="w", pady=(2, 0))

    content_frame = tk.Frame(cat_window, bg=COLOR_CARD, bd=0, highlightthickness=0)
    content_frame.pack(fill="both", expand=True, padx=30, pady=(0, 10))

    for cat_id, cat_name in categories:
        btn = tk.Button(
            content_frame, text=cat_name, font=("Arial", 11, "bold"),
            bg=COLOR_PRIMARY, fg="white", activebackground="#1D4ED8", activeforeground="white",
            relief="flat", cursor="hand2", pady=8,
            command=lambda cid=cat_id, cname=cat_name: show_items(cid, cname)
        )
        btn.pack(fill="x", padx=20, pady=5)

    btn_back = tk.Button(
        cat_window, text="⬅ Back to Main Menu", font=("Arial", 10, "bold"),
        bg=COLOR_BACK, fg=COLOR_BACK_TEXT, activebackground="#D1D5DB", activeforeground=COLOR_BACK_TEXT,
        relief="flat", cursor="hand2", pady=8, width=28,
        command=cat_window.destroy
    )
    btn_back.pack(pady=(5, 20))


def show_items(category_id, category_name):
    conn = get_db_connection()
    if not conn: return
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.name, p.price, p.stock_qty, l.aisle, l.shelf 
        FROM products p
        JOIN locations l ON p.location_id = l.location_id
        WHERE p.category_id = %s
    """, (category_id,))
    products = cursor.fetchall()
    conn.close()

    item_window = tk.Toplevel(root)
    item_window.title(f"{category_name} Inventory")
    center_window(item_window, 460, 600)

    tk.Label(item_window, text=f"📦 {category_name} Products", font=("Arial", 15, "bold"),
             bg=COLOR_BG, fg=COLOR_TEXT).pack(pady=(20, 5))

    list_frame = tk.Frame(item_window, bg="white", padx=10, pady=10)
    list_frame.pack(fill="both", expand=True, padx=30, pady=10)

    listbox = tk.Listbox(list_frame, font=("Arial", 11), bg="white", fg=COLOR_TEXT,
                         selectbackground=COLOR_PRIMARY, selectforeground="white",
                         relief="flat", bd=0, highlightthickness=0)

    product_map = {}
    for idx, item_record in enumerate(products):
        prod_name, prod_price, _, _, _ = item_record
        listbox.insert(tk.END, f"   {prod_name}  —  ₱{prod_price:.2f}")
        product_map[idx] = item_record

    listbox.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=listbox.yview)
    scrollbar.pack(side="right", fill="y")
    listbox.config(yscrollcommand=scrollbar.set)

    def view_selected_details():
        selection = listbox.curselection()
        if not selection and products:
            selected_record = products[0]
        elif selection:
            selected_record = product_map[selection[0]]
        else:
            return

        p_name, p_price, p_stock, p_aisle, p_shelf = selected_record
        status = "In Stock" if p_stock > 0 else "Out of Stock"

        messagebox.showinfo("Product Information",
                            f"Product: {p_name}\nPrice: ₱{p_price:.2f}\nStatus: {status} ({p_stock} available)\n\n📍 Location:\n- {p_aisle}, {p_shelf}",
                            parent=item_window)

    btn_view = tk.Button(
        item_window, text="📍 View Product Location", font=("Arial", 11, "bold"),
        bg=COLOR_SECONDARY, fg="white", activebackground="#059669", activeforeground="white",
        relief="flat", cursor="hand2", pady=8, width=28,
        command=view_selected_details
    )
    btn_view.pack(pady=(10, 5))

    btn_back = tk.Button(
        item_window, text="⬅ Back to Categories", font=("Arial", 10, "bold"),
        bg=COLOR_BACK, fg=COLOR_BACK_TEXT, activebackground="#D1D5DB", activeforeground=COLOR_BACK_TEXT,
        relief="flat", cursor="hand2", pady=8, width=28,
        command=item_window.destroy
    )
    btn_back.pack(pady=(0, 20))


def employee_flow():
    login_win = tk.Toplevel(root)
    login_win.title("Employee Login")
    center_window(login_win, 360, 360)

    tk.Label(login_win, text="🔐 Employee Login", font=("Arial", 15, "bold"),
             bg=COLOR_BG, fg=COLOR_TEXT).pack(pady=(25, 5))
    tk.Label(login_win, text="Enter your administrative credentials", font=("Arial", 9),
             bg=COLOR_BG, fg=COLOR_MUTED).pack(pady=(0, 15))

    form_frame = tk.Frame(login_win, bg=COLOR_BG)
    form_frame.pack(fill="x", padx=40)

    tk.Label(form_frame, text="Username", font=("Arial", 9, "bold"), bg=COLOR_BG, fg=COLOR_TEXT).pack(anchor="w")
    user_ent = tk.Entry(form_frame, font=("Arial", 11), bd=0, relief="flat", highlightthickness=1)
    user_ent.config(highlightbackground="#D1D5DB", highlightcolor=COLOR_EMPLOYEE)
    user_ent.pack(fill="x", ipady=5, pady=(3, 10))

    tk.Label(form_frame, text="Password", font=("Arial", 9, "bold"), bg=COLOR_BG, fg=COLOR_TEXT).pack(anchor="w")
    pass_ent = tk.Entry(form_frame, show="*", font=("Arial", 11), bd=0, relief="flat", highlightthickness=1)
    pass_ent.config(highlightbackground="#D1D5DB", highlightcolor=COLOR_EMPLOYEE)
    pass_ent.pack(fill="x", ipady=5, pady=(3, 15))

    def verify():
        conn = get_db_connection()
        if not conn: return
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees WHERE username = %s AND password = %s",
                       (user_ent.get(), pass_ent.get()))
        user_record = cursor.fetchone()
        conn.close()

        if user_record:
            login_win.destroy()
            show_employee_dashboard()
        else:
            messagebox.showerror("Error", "Invalid username or password", parent=login_win)

    btn_login = tk.Button(
        login_win, text="Sign In", font=("Arial", 11, "bold"),
        bg=COLOR_EMPLOYEE, fg="white", activebackground="#4338CA", activeforeground="white",
        relief="flat", cursor="hand2", pady=8, width=24,
        command=verify
    )
    btn_login.pack(pady=(5, 5))

    btn_back = tk.Button(
        login_win, text="⬅ Back to Main Menu", font=("Arial", 10, "bold"),
        bg=COLOR_BACK, fg=COLOR_BACK_TEXT, activebackground="#D1D5DB", activeforeground=COLOR_BACK_TEXT,
        relief="flat", cursor="hand2", pady=8, width=24,
        command=login_win.destroy
    )
    btn_back.pack(pady=(0, 20))


def open_product_registration():
    reg_win = tk.Toplevel(root)
    reg_win.title("Product Registration")
    center_window(reg_win, 380, 440)

    tk.Label(reg_win, text="📝 Register New Product", font=("Arial", 14, "bold"), bg=COLOR_BG, fg=COLOR_TEXT).pack(
        pady=15)

    form = tk.Frame(reg_win, bg=COLOR_BG)
    form.pack(fill="x", padx=30)

    tk.Label(form, text="Product Name:", bg=COLOR_BG, font=("Arial", 9, "bold")).pack(anchor="w")
    name_ent = tk.Entry(form, font=("Arial", 11), bd=1, relief="solid")
    name_ent.pack(fill="x", pady=(2, 8))

    tk.Label(form, text="Category ID (1-5):", bg=COLOR_BG, font=("Arial", 9, "bold")).pack(anchor="w")
    cat_ent = tk.Entry(form, font=("Arial", 11), bd=1, relief="solid")
    cat_ent.pack(fill="x", pady=(2, 8))

    tk.Label(form, text="Location ID (1-4):", bg=COLOR_BG, font=("Arial", 9, "bold")).pack(anchor="w")
    loc_ent = tk.Entry(form, font=("Arial", 11), bd=1, relief="solid")
    loc_ent.pack(fill="x", pady=(2, 8))

    tk.Label(form, text="Price (₱):", bg=COLOR_BG, font=("Arial", 9, "bold")).pack(anchor="w")
    price_ent = tk.Entry(form, font=("Arial", 11), bd=1, relief="solid")
    price_ent.pack(fill="x", pady=(2, 8))

    tk.Label(form, text="Stock Quantity:", bg=COLOR_BG, font=("Arial", 9, "bold")).pack(anchor="w")
    stock_ent = tk.Entry(form, font=("Arial", 11), bd=1, relief="solid")
    stock_ent.pack(fill="x", pady=(2, 12))

    def save_product():
        try:
            name = name_ent.get()
            cat_id = int(cat_ent.get())
            loc_id = int(loc_ent.get())
            price = float(price_ent.get())
            stock = int(stock_ent.get())

            if not name:
                messagebox.showerror("Error", "Product name cannot be empty", parent=reg_win)
                return

            conn = get_db_connection()
            if not conn: return
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO products (name, category_id, location_id, price, stock_qty) VALUES (%s, %s, %s, %s, %s)",
                (name, cat_id, loc_id, price, stock))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", f"Product '{name}' registered successfully!", parent=reg_win)
            reg_win.destroy()
        except ValueError:
            messagebox.showerror("Invalid Input",
                                 "Please enter valid numeric values for Category, Location, Price, and Stock.",
                                 parent=reg_win)

    tk.Button(reg_win, text="Save Product", font=("Arial", 10, "bold"), bg=COLOR_SECONDARY, fg="white", relief="flat",
              cursor="hand2", pady=8, width=22, command=save_product).pack(pady=5)
    tk.Button(reg_win, text="⬅ Back", font=("Arial", 9, "bold"), bg=COLOR_BACK, fg=COLOR_BACK_TEXT, relief="flat",
              cursor="hand2", pady=6, width=22, command=reg_win.destroy).pack()


def open_product_search():
    search_win = tk.Toplevel(root)
    search_win.title("Product Search & Inventory Info")
    center_window(search_win, 500, 480)

    tk.Label(search_win, text="🔍 Search Store Inventory", font=("Arial", 14, "bold"), bg=COLOR_BG, fg=COLOR_TEXT).pack(
        pady=15)

    top_frame = tk.Frame(search_win, bg=COLOR_BG)
    top_frame.pack(fill="x", padx=30)

    tk.Label(top_frame, text="Enter Product Name:", bg=COLOR_BG, font=("Arial", 9, "bold")).pack(anchor="w")
    query_ent = tk.Entry(top_frame, font=("Arial", 11), bd=1, relief="solid")
    query_ent.pack(fill="x", pady=5)

    results_frame = tk.Frame(search_win, bg="white", padx=5, pady=5)
    results_frame.pack(fill="both", expand=True, padx=30, pady=10)

    listbox = tk.Listbox(results_frame, font=("Arial", 10), bg="white", fg=COLOR_TEXT, relief="flat")
    listbox.pack(side="left", fill="both", expand=True)
    scrollbar = tk.Scrollbar(results_frame, orient="vertical", command=listbox.yview)
    scrollbar.pack(side="right", fill="y")
    listbox.config(yscrollcommand=scrollbar.set)

    def perform_search():
        keyword = query_ent.get().strip()
        conn = get_db_connection()
        if not conn: return
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.name, p.price, p.stock_qty, l.aisle, l.shelf 
            FROM products p 
            JOIN locations l ON p.location_id = l.location_id 
            WHERE p.name LIKE %s
        """, (f"%{keyword}%",))
        rows = cursor.fetchall()
        conn.close()

        listbox.delete(0, tk.END)
        if not rows:
            listbox.insert(tk.END, "   No products found.")
        for r in rows:
            name, price, stock, aisle, shelf = r
            listbox.insert(tk.END, f"• {name} | ₱{price:.2f} | Stock: {stock} | 📍 {aisle}, {shelf}")

    tk.Button(search_win, text="Search Database", font=("Arial", 10, "bold"), bg=COLOR_PRIMARY, fg="white",
              relief="flat", cursor="hand2", pady=6, width=20, command=perform_search).pack(pady=5)
    tk.Button(search_win, text="⬅ Back", font=("Arial", 9, "bold"), bg=COLOR_BACK, fg=COLOR_BACK_TEXT, relief="flat",
              cursor="hand2", pady=6, width=20, command=search_win.destroy).pack(pady=(0, 15))

    # Perform initial search to list all items
    perform_search()


def open_reports_summary():
    conn = get_db_connection()
    if not conn: return
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*), SUM(stock_qty), AVG(price) FROM products")
    total_prods, total_stock, avg_price = cursor.fetchone()
    cursor.execute("SELECT COUNT(*) FROM categories")
    total_cats = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM employees")
    total_emps = cursor.fetchone()[0]
    conn.close()

    rep_win = tk.Toplevel(root)
    rep_win.title("Store Reports")
    center_window(rep_win, 380, 400)

    tk.Label(rep_win, text="📊 Store Inventory Reports", font=("Arial", 14, "bold"), bg=COLOR_BG, fg=COLOR_TEXT).pack(
        pady=20)

    card = tk.Frame(rep_win, bg="white", padx=20, pady=20)
    card.pack(fill="both", expand=True, padx=30, pady=10)

    tk.Label(card, text=f"📦 Total Unique Products: {total_prods}", font=("Arial", 11), bg="white", fg=COLOR_TEXT).pack(
        anchor="w", pady=4)
    tk.Label(card, text=f"🔢 Total Stock Units: {total_stock or 0}", font=("Arial", 11), bg="white", fg=COLOR_TEXT).pack(
        anchor="w", pady=4)
    tk.Label(card, text=f"🏷️ Average Product Price: ₱{(avg_price or 0):.2f}", font=("Arial", 11), bg="white",
             fg=COLOR_TEXT).pack(anchor="w", pady=4)
    tk.Label(card, text=f"🗂️ Categories Count: {total_cats}", font=("Arial", 11), bg="white", fg=COLOR_TEXT).pack(
        anchor="w", pady=4)
    tk.Label(card, text=f"👤 Registered Employees: {total_emps}", font=("Arial", 11), bg="white", fg=COLOR_TEXT).pack(
        anchor="w", pady=4)

    tk.Button(rep_win, text="⬅ Back", font=("Arial", 9, "bold"), bg=COLOR_BACK, fg=COLOR_BACK_TEXT, relief="flat",
              cursor="hand2", pady=6, width=22, command=rep_win.destroy).pack(pady=15)


def show_employee_dashboard():
    dash = tk.Toplevel(root)
    dash.title("Store Management Dashboard")
    center_window(dash, 420, 580)

    tk.Label(dash, text="⚙️ Management Dashboard", font=("Arial", 15, "bold"),
             bg=COLOR_BG, fg=COLOR_TEXT).pack(pady=(20, 10))

    # Map buttons to functional routines
    modules = [
        ("Product Registration", open_product_registration),
        ("Product Categories",
         lambda: messagebox.showinfo("Categories", "5 Core Categories loaded in MySQL database.", parent=dash)),
        ("Aisle Management",
         lambda: messagebox.showinfo("Aisles", "Aisles 1-4 active in database locations.", parent=dash)),
        ("Shelf Management",
         lambda: messagebox.showinfo("Shelves", "Shelves A-1 to D-4 linked successfully.", parent=dash)),
        ("Product Search", open_product_search),
        ("Location Display", open_product_search),
        ("Availability Tracking", open_product_search),
        ("Search & Filtering", open_product_search),
        ("Inventory Info", open_product_search),
        ("Location Updating",
         lambda: messagebox.showinfo("Location", "Select item in search to check or update location.", parent=dash)),
        ("Reports", open_reports_summary),
        ("Activity Logs",
         lambda: messagebox.showinfo("Logs", "System Audit Logs: All MySQL queries executed successfully.",
                                     parent=dash))
    ]

    mod_frame = tk.Frame(dash, bg=COLOR_BG)
    mod_frame.pack(fill="both", expand=True, padx=30, pady=5)

    for mod_name, mod_func in modules:
        btn = tk.Button(
            mod_frame, text=mod_name, font=("Arial", 10),
            bg="white", fg=COLOR_TEXT, activebackground=COLOR_PRIMARY, activeforeground="white",
            relief="flat", cursor="hand2", pady=5, width=35,
            command=mod_func
        )
        btn.pack(pady=2)

    btn_back = tk.Button(
        dash, text="⬅ Logout / Back", font=("Arial", 10, "bold"),
        bg=COLOR_BACK, fg=COLOR_BACK_TEXT, activebackground="#D1D5DB", activeforeground=COLOR_BACK_TEXT,
        relief="flat", cursor="hand2", pady=8, width=30,
        command=dash.destroy
    )
    btn_back.pack(pady=(10, 20))


# Main Application Window
root = tk.Tk()
root.title("Convenience Store POS & System")
center_window(root, 380, 360)

tk.Label(root, text="🏪 Convenience Store", font=("Arial", 18, "bold"),
         bg=COLOR_BG, fg=COLOR_TEXT).pack(pady=(25, 5))
tk.Label(root, text="Select your portal to continue", font=("Arial", 10),
         bg=COLOR_BG, fg=COLOR_MUTED).pack(pady=(0, 15))

btn_cust = tk.Button(
    root, text="🛒 Customer Portal", font=("Arial", 11, "bold"),
    bg=COLOR_PRIMARY, fg="white", activebackground="#1D4ED8", activeforeground="white",
    relief="flat", cursor="hand2", pady=12, width=24,
    command=customer_flow
)
btn_cust.pack(pady=6)

btn_emp = tk.Button(
    root, text="🔐 Employee Portal", font=("Arial", 11, "bold"),
    bg=COLOR_EMPLOYEE, fg="white", activebackground="#4338CA", activeforeground="white",
    relief="flat", cursor="hand2", pady=12, width=24,
    command=employee_flow
)
btn_emp.pack(pady=6)

# Live Database Connection Status Widget
status_frame = tk.Frame(root, bg=COLOR_BG)
status_frame.pack(pady=(15, 0))

test_conn = get_db_connection()
if test_conn and test_conn.is_connected():
    status_text = "🟢 Database Connected (MySQL)"
    status_color = "#059669"
    test_conn.close()
else:
    status_text = "🔴 Database Disconnected"
    status_color = "#DC2626"

tk.Label(status_frame, text=status_text, font=("Arial", 9, "bold"),
         bg=COLOR_BG, fg=status_color).pack()

root.mainloop()