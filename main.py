import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date, timedelta
from tkcalendar import Calendar

# Database setup
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Vedant@12'
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS diet_management")
            cursor.execute("USE diet_management")
            
            # Users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    age INT,
                    weight DECIMAL(5,2),
                    height DECIMAL(5,2),
                    gender VARCHAR(10),
                    activity_level VARCHAR(20),
                    goal VARCHAR(20),
                    daily_calories INT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Food items table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS food_items (
                    food_id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    calories DECIMAL(10,2) NOT NULL,
                    protein DECIMAL(10,2),
                    carbohydrates DECIMAL(10,2),
                    fats DECIMAL(10,2),
                    category VARCHAR(50),
                    serving_size VARCHAR(50),
                    user_id INT,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                )
            """)
            
            # Meals table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS meals (
                    meal_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    meal_type VARCHAR(50) NOT NULL,
                    date DATE NOT NULL,
                    notes TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                )
            """)
            
            # Meal items table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS meal_items (
                    meal_item_id INT AUTO_INCREMENT PRIMARY KEY,
                    meal_id INT NOT NULL,
                    food_id INT NOT NULL,
                    quantity DECIMAL(10,2) NOT NULL,
                    FOREIGN KEY (meal_id) REFERENCES meals(meal_id) ON DELETE CASCADE,
                    FOREIGN KEY (food_id) REFERENCES food_items(food_id) ON DELETE CASCADE
                )
            """)
            
            connection.commit()
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

class DietManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Healthy Diet Management System")
        self.root.geometry("1100x700")
        self.root.minsize(1000, 600)
        self.current_user = None
        self.connection = create_connection()
        
        self.configure_styles()
        self.setup_ui()
    
    def configure_styles(self):
        """Configure ttk styles for a modern look"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # General styles
        style.configure('.', font=('Segoe UI', 10))
        style.configure('TFrame', background='#f5f5f5')
        style.configure('TLabel', background='#f5f5f5', font=('Segoe UI', 10))
        style.configure('TButton', font=('Segoe UI', 10), padding=5)
        style.configure('Header.TLabel', font=('Segoe UI', 14, 'bold'))
        style.configure('Secondary.TButton', background='#e1e1e1')
        style.configure('TEntry', padding=5)
        style.configure('TCombobox', padding=5)
        
        # Treeview styles
        style.configure('Treeview', font=('Segoe UI', 9), rowheight=25)
        style.configure('Treeview.Heading', font=('Segoe UI', 9, 'bold'))
        style.map('Treeview', background=[('selected', '#0078d7')])
        
        # Notebook style (for potential future tabs)
        style.configure('TNotebook', background='#f5f5f5')
        style.configure('TNotebook.Tab', padding=[10, 5], font=('Segoe UI', 10))
        
        # Custom card style
        style.configure('Card.TFrame', background='white', relief=tk.RIDGE, borderwidth=1)
    
    def setup_ui(self):
        """Setup the main UI container"""
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.show_login_screen()
    
    def clear_frame(self):
        """Clear all widgets from the main frame"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def show_login_screen(self):
        """Display the login screen"""
        self.clear_frame()
        
        # Main container
        login_container = ttk.Frame(self.main_frame)
        login_container.pack(expand=True, pady=50)
        
        # Header
        ttk.Label(login_container, text="Healthy Diet Management", 
                 style='Header.TLabel').grid(row=0, column=0, columnspan=2, pady=20)
        
        # Login form
        ttk.Label(login_container, text="Username:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        self.username_entry = ttk.Entry(login_container, width=25)
        self.username_entry.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(login_container, text="Password:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        self.password_entry = ttk.Entry(login_container, show="*", width=25)
        self.password_entry.grid(row=2, column=1, padx=10, pady=5)
        
        # Button frame
        button_frame = ttk.Frame(login_container)
        button_frame.grid(row=3, column=0, columnspan=2, pady=15)
        
        login_btn = ttk.Button(button_frame, text="Login", command=self.login, width=15)
        login_btn.pack(side=tk.LEFT, padx=5)
        
        register_btn = ttk.Button(button_frame, text="Register", 
                                command=self.show_register_screen, 
                                style='Secondary.TButton', width=15)
        register_btn.pack(side=tk.LEFT, padx=5)
        
        self.username_entry.focus_set()
        self.root.bind('<Return>', lambda event: self.login())
    
    def show_register_screen(self):
        """Display the registration screen"""
        self.clear_frame()
        
        # Main container with scrollbar
        container = ttk.Frame(self.main_frame)
        container.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Registration form
        ttk.Label(scrollable_frame, text="Create New Account", 
                 style='Header.TLabel').grid(row=0, column=0, columnspan=2, pady=10)
        
        # Form fields
        fields = [
            ("Username:", "reg_username", None),
            ("Password:", "reg_password", {"show": "*"}),
            ("Email:", "reg_email", None),
            ("Age:", "reg_age", None),
            ("Weight (kg):", "reg_weight", None),
            ("Height (cm):", "reg_height", None),
            ("Gender:", "reg_gender", {"values": ["Male", "Female", "Other"]}),
            ("Activity Level:", "reg_activity", {"values": ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"]}),
            ("Goal:", "reg_goal", {"values": ["Weight Loss", "Weight Maintenance", "Weight Gain"]})
        ]
        
        for i, (label_text, attr_name, combo_args) in enumerate(fields, start=1):
            ttk.Label(scrollable_frame, text=label_text).grid(row=i, column=0, padx=10, pady=5, sticky=tk.E)
            
            if combo_args:
                widget = ttk.Combobox(scrollable_frame, width=22, **combo_args)
                if "values" in combo_args:
                    widget.current(0)
            else:
                widget = ttk.Entry(scrollable_frame, width=25)
            
            widget.grid(row=i, column=1, padx=10, pady=5, sticky=tk.W)
            setattr(self, attr_name, widget)
        
        # Button frame
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=15)
        
        register_btn = ttk.Button(button_frame, text="Register", command=self.register, width=15)
        register_btn.pack(side=tk.LEFT, padx=5)
        
        back_btn = ttk.Button(button_frame, text="Back to Login", 
                            command=self.show_login_screen, 
                            style='Secondary.TButton', width=15)
        back_btn.pack(side=tk.LEFT, padx=5)
        
        self.reg_username.focus_set()
    
    def show_dashboard(self):
        """Display the main dashboard"""
        self.clear_frame()
        
        # Create main container with sidebar and content
        main_container = ttk.Frame(self.main_frame)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar menu
        sidebar = ttk.Frame(main_container, width=200, style='TFrame')
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # User info at top of sidebar
        user_frame = ttk.Frame(sidebar, padding=10, style='Card.TFrame')
        user_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(user_frame, text=f"Welcome,\n{self.current_user[1]}!", 
                 font=('Segoe UI', 10, 'bold'), justify=tk.CENTER).pack()
        
        # Menu buttons
        menu_buttons = [
            ("Dashboard", self.show_dashboard),
            ("Food Database", self.show_food_database),
            ("Add Meal", self.show_add_meal),
            ("Daily Log", self.show_daily_log),
            ("Reports", self.show_reports),
            ("Profile", self.show_profile),
            ("Logout", self.logout)
        ]
        
        for text, command in menu_buttons:
            btn = ttk.Button(sidebar, text=text, command=command)
            btn.pack(fill=tk.X, pady=2)
        
        # Content area
        content = ttk.Frame(main_container)
        content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Dashboard title
        ttk.Label(content, text="Dashboard Overview", 
                 style='Header.TLabel').pack(pady=(0, 15))
        
        # Today's summary card
        summary_card = ttk.Frame(content, padding=10, style='Card.TFrame')
        summary_card.pack(fill=tk.X, pady=5)
        
        ttk.Label(summary_card, text="Today's Summary", 
                 font=('Segoe UI', 11, 'bold')).pack(anchor=tk.W)
        
        today = datetime.now().strftime("%Y-%m-%d")
        total_calories = self.get_daily_calories(today)
        goal_calories = self.current_user[10] if self.current_user[10] else 2000
        
        # Progress bar with labels
        progress_frame = ttk.Frame(summary_card)
        progress_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(progress_frame, text=f"Calories: {total_calories}/{goal_calories}").pack(anchor=tk.W)
        
        progress = ttk.Progressbar(progress_frame, orient=tk.HORIZONTAL, 
                                 length=300, mode='determinate')
        progress.pack(fill=tk.X, pady=5)
        progress['value'] = min((total_calories / goal_calories) * 100, 100)
        
        # Recent meals card
        meals_card = ttk.Frame(content, padding=10, style='Card.TFrame')
        meals_card.pack(fill=tk.BOTH, expand=True, pady=5)
        
        ttk.Label(meals_card, text="Recent Meals", 
                 font=('Segoe UI', 11, 'bold')).pack(anchor=tk.W)
        
        recent_meals = self.get_recent_meals()
        
        if not recent_meals:
            ttk.Label(meals_card, text="No recent meals found").pack(pady=10)
        else:
            for meal in recent_meals:
                meal_frame = ttk.Frame(meals_card, padding=5)
                meal_frame.pack(fill=tk.X, pady=2)
                
                ttk.Label(meal_frame, text=f"{meal[2]} - {meal[3]}",
                         font=('Segoe UI', 9)).pack(side=tk.LEFT, padx=5)
                
                ttk.Label(meal_frame, text=f"{self.get_meal_calories(meal[0])} calories",
                         font=('Segoe UI', 9, 'bold')).pack(side=tk.RIGHT, padx=5)
    
    def show_food_database(self):
        """Display the food database screen"""
        self.clear_frame()
        
        # Main container
        main_container = ttk.Frame(self.main_frame)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar
        sidebar = ttk.Frame(main_container, width=200, style='TFrame')
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Menu buttons
        menu_buttons = [
            ("Dashboard", self.show_dashboard),
            ("Food Database", self.show_food_database),
            ("Add Meal", self.show_add_meal),
            ("Daily Log", self.show_daily_log),
            ("Reports", self.show_reports),
            ("Profile", self.show_profile),
            ("Logout", self.logout)
        ]
        
        for text, command in menu_buttons:
            btn = ttk.Button(sidebar, text=text, command=command)
            btn.pack(fill=tk.X, pady=2)
        
        # Content area
        content = ttk.Frame(main_container)
        content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Food database title
        ttk.Label(content, text="Food Database", 
                 style='Header.TLabel').pack(pady=10)
        
        # Search frame
        search_frame = ttk.Frame(content)
        search_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.food_search_entry = ttk.Entry(search_frame)
        self.food_search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(search_frame, text="Search", command=self.search_food).pack(side=tk.LEFT, padx=5)
        
        # Add food button
        ttk.Button(content, text="Add New Food", command=self.show_add_food).pack(pady=5, anchor=tk.E)
        
        # Food list treeview
        self.food_tree = ttk.Treeview(content, columns=("name", "calories", "protein", "carbs", "fats", "category"), 
                                     show="headings", selectmode="browse")
        self.food_tree.heading("name", text="Name")
        self.food_tree.heading("calories", text="Calories")
        self.food_tree.heading("protein", text="Protein (g)")
        self.food_tree.heading("carbs", text="Carbs (g)")
        self.food_tree.heading("fats", text="Fats (g)")
        self.food_tree.heading("category", text="Category")
        
        # Set column widths
        self.food_tree.column("name", width=200)
        self.food_tree.column("calories", width=80)
        self.food_tree.column("protein", width=80)
        self.food_tree.column("carbs", width=80)
        self.food_tree.column("fats", width=80)
        self.food_tree.column("category", width=120)
        
        self.food_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Load food items
        self.load_food_items()
    
    def show_add_food(self):
        """Display the add food form"""
        self.clear_frame()
        
        # Main container
        main_container = ttk.Frame(self.main_frame)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar
        sidebar = ttk.Frame(main_container, width=200, style='TFrame')
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Menu buttons
        menu_buttons = [
            ("Dashboard", self.show_dashboard),
            ("Food Database", self.show_food_database),
            ("Add Meal", self.show_add_meal),
            ("Daily Log", self.show_daily_log),
            ("Reports", self.show_reports),
            ("Profile", self.show_profile),
            ("Logout", self.logout)
        ]
        
        for text, command in menu_buttons:
            btn = ttk.Button(sidebar, text=text, command=command)
            btn.pack(fill=tk.X, pady=2)
        
        # Content area
        content = ttk.Frame(main_container)
        content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Add food title
        ttk.Label(content, text="Add New Food", 
                 style='Header.TLabel').pack(pady=10)
        
        # Form frame
        form_frame = ttk.Frame(content, padding=10, style='Card.TFrame')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Form fields
        fields = [
            ("Name:", "food_name", None),
            ("Calories:", "food_calories", None),
            ("Protein (g):", "food_protein", None),
            ("Carbs (g):", "food_carbs", None),
            ("Fats (g):", "food_fats", None),
            ("Category:", "food_category", {"values": ["Vegetables", "Fruits", "Grains", "Protein", "Dairy", "Fats/Oils", "Sweets", "Beverages", "Other"]}),
            ("Serving Size:", "food_serving", None)
        ]
        
        for i, (label_text, attr_name, combo_args) in enumerate(fields):
            ttk.Label(form_frame, text=label_text).grid(row=i, column=0, padx=5, pady=5, sticky=tk.E)
            
            if combo_args:
                widget = ttk.Combobox(form_frame, width=25, **combo_args)
            else:
                widget = ttk.Entry(form_frame, width=25)
            
            widget.grid(row=i, column=1, padx=5, pady=5, sticky=tk.W)
            setattr(self, attr_name, widget)
        
        # Button frame
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Save Food", command=self.save_food).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.show_food_database, 
                  style='Secondary.TButton').pack(side=tk.LEFT, padx=5)
        
        self.food_name.focus_set()
    
    def show_add_meal(self):
        """Display the add meal form"""
        self.clear_frame()
        
        # Main container
        main_container = ttk.Frame(self.main_frame)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar
        sidebar = ttk.Frame(main_container, width=200, style='TFrame')
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Menu buttons
        menu_buttons = [
            ("Dashboard", self.show_dashboard),
            ("Food Database", self.show_food_database),
            ("Add Meal", self.show_add_meal),
            ("Daily Log", self.show_daily_log),
            ("Reports", self.show_reports),
            ("Profile", self.show_profile),
            ("Logout", self.logout)
        ]
        
        for text, command in menu_buttons:
            btn = ttk.Button(sidebar, text=text, command=command)
            btn.pack(fill=tk.X, pady=2)
        
        # Content area
        content = ttk.Frame(main_container)
        content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Add meal title
        ttk.Label(content, text="Add Meal", 
                 style='Header.TLabel').pack(pady=10)
        
        # Meal details frame
        details_frame = ttk.Frame(content, padding=10, style='Card.TFrame')
        details_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Meal type
        ttk.Label(details_frame, text="Meal Type:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.meal_type = ttk.Combobox(details_frame, values=["Breakfast", "Lunch", "Dinner", "Snack"], width=23)
        self.meal_type.grid(row=0, column=1, sticky=tk.W, pady=2)
        
        # Date
        ttk.Label(details_frame, text="Date:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.meal_date = ttk.Entry(details_frame, width=25)
        self.meal_date.insert(0, date.today().strftime("%Y-%m-%d"))
        self.meal_date.grid(row=1, column=1, sticky=tk.W, pady=2)
        
        # Notes
        ttk.Label(details_frame, text="Notes:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.meal_notes = ttk.Entry(details_frame, width=25)
        self.meal_notes.grid(row=2, column=1, sticky=tk.W, pady=2)
        
        # Food selection frame
        ttk.Label(content, text="Add Food Items:", 
                 font=('Segoe UI', 11)).pack(pady=5, anchor=tk.W)
        
        selection_frame = ttk.Frame(content, padding=10, style='Card.TFrame')
        selection_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Food dropdown
        ttk.Label(selection_frame, text="Food:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.meal_food = ttk.Combobox(selection_frame)
        self.meal_food.grid(row=0, column=1, sticky=tk.EW, pady=2, padx=5)
        
        # Quantity
        ttk.Label(selection_frame, text="Quantity:").grid(row=0, column=2, sticky=tk.W, pady=2)
        self.meal_quantity = ttk.Entry(selection_frame, width=5)
        self.meal_quantity.insert(0, "1")
        self.meal_quantity.grid(row=0, column=3, sticky=tk.W, pady=2)
        
        # Add button
        ttk.Button(selection_frame, text="Add", command=self.add_food_to_meal).grid(row=0, column=4, padx=5)
        
        # Meal items treeview
        self.meal_items_tree = ttk.Treeview(content, columns=("name", "calories", "quantity", "total"), 
                                          show="headings", selectmode="browse")
        self.meal_items_tree.heading("name", text="Food")
        self.meal_items_tree.heading("calories", text="Calories per unit")
        self.meal_items_tree.heading("quantity", text="Quantity")
        self.meal_items_tree.heading("total", text="Total Calories")
        
        # Set column widths
        self.meal_items_tree.column("name", width=200)
        self.meal_items_tree.column("calories", width=120)
        self.meal_items_tree.column("quantity", width=80)
        self.meal_items_tree.column("total", width=100)
        
        self.meal_items_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Summary frame
        summary_frame = ttk.Frame(content)
        summary_frame.pack(fill=tk.X, pady=5)
        
        self.meal_total_label = ttk.Label(summary_frame, text="Total Calories: 0", 
                                        font=('Segoe UI', 10, 'bold'))
        self.meal_total_label.pack(side=tk.LEFT)
        
        # Button frame
        button_frame = ttk.Frame(content)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Save Meal", command=self.save_meal).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.show_dashboard, 
                  style='Secondary.TButton').pack(side=tk.LEFT, padx=5)
        
        # Load foods for dropdown
        self.load_food_combobox()
        self.meal_foods = []  # Stores food items for the current meal
    
    def show_daily_log(self):
        """Display the daily log screen"""
        self.clear_frame()
        
        # Main container
        main_container = ttk.Frame(self.main_frame)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar
        sidebar = ttk.Frame(main_container, width=200, style='TFrame')
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Menu buttons
        menu_buttons = [
            ("Dashboard", self.show_dashboard),
            ("Food Database", self.show_food_database),
            ("Add Meal", self.show_add_meal),
            ("Daily Log", self.show_daily_log),
            ("Reports", self.show_reports),
            ("Profile", self.show_profile),
            ("Logout", self.logout)
        ]
        
        for text, command in menu_buttons:
            btn = ttk.Button(sidebar, text=text, command=command)
            btn.pack(fill=tk.X, pady=2)
        
        # Content area
        content = ttk.Frame(main_container)
        content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Daily log title
        ttk.Label(content, text="Daily Log", 
                 style='Header.TLabel').pack(pady=10)
        
        # Date selection frame
        date_frame = ttk.Frame(content, padding=10, style='Card.TFrame')
        date_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(date_frame, text="Select Date:").pack(side=tk.LEFT, padx=5)
        self.log_date = Calendar(date_frame, selectmode='day', date_pattern='y-mm-dd')
        self.log_date.pack(side=tk.LEFT, padx=5)
        ttk.Button(date_frame, text="Load", command=self.load_daily_log).pack(side=tk.LEFT, padx=5)
        
        # Summary frame
        self.log_summary_frame = ttk.Frame(content, padding=10, style='Card.TFrame')
        self.log_summary_frame.pack(fill=tk.X, pady=5)
        
        # Meals frame
        self.log_meals_frame = ttk.Frame(content)
        self.log_meals_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Load today's log by default
        self.load_daily_log()
    
    def show_reports(self):
        """Display the reports screen"""
        self.clear_frame()
        
        # Main container
        main_container = ttk.Frame(self.main_frame)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar
        sidebar = ttk.Frame(main_container, width=200, style='TFrame')
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Menu buttons
        menu_buttons = [
            ("Dashboard", self.show_dashboard),
            ("Food Database", self.show_food_database),
            ("Add Meal", self.show_add_meal),
            ("Daily Log", self.show_daily_log),
            ("Reports", self.show_reports),
            ("Profile", self.show_profile),
            ("Logout", self.logout)
        ]
        
        for text, command in menu_buttons:
            btn = ttk.Button(sidebar, text=text, command=command)
            btn.pack(fill=tk.X, pady=2)
        
        # Content area
        content = ttk.Frame(main_container)
        content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Reports title
        ttk.Label(content, text="Reports", 
                 style='Header.TLabel').pack(pady=10)
        
        # Report controls frame
        controls_frame = ttk.Frame(content, padding=10, style='Card.TFrame')
        controls_frame.pack(fill=tk.X, pady=5)
        
        # Time period selection
        period_frame = ttk.Frame(controls_frame)
        period_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(period_frame, text="Time Period:").pack(side=tk.LEFT, padx=5)
        self.report_period = ttk.Combobox(period_frame, values=["Last 7 Days", "Last 30 Days", "This Month", "Custom"])
        self.report_period.pack(side=tk.LEFT, padx=5)
        self.report_period.bind("<<ComboboxSelected>>", self.update_report_dates)
        
        # Custom date frame
        self.custom_date_frame = ttk.Frame(controls_frame)
        
        ttk.Label(self.custom_date_frame, text="From:").pack(side=tk.LEFT, padx=5)
        self.report_start_date = Calendar(self.custom_date_frame, selectmode='day', date_pattern='y-mm-dd')
        self.report_start_date.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(self.custom_date_frame, text="To:").pack(side=tk.LEFT, padx=5)
        self.report_end_date = Calendar(self.custom_date_frame, selectmode='day', date_pattern='y-mm-dd')
        self.report_end_date.pack(side=tk.LEFT, padx=5)
        
        # Report type
        report_type_frame = ttk.Frame(controls_frame)
        report_type_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(report_type_frame, text="Report Type:").pack(side=tk.LEFT, padx=5)
        self.report_type = ttk.Combobox(report_type_frame, values=["Calorie Summary", "Macronutrients", "Meal Types", "Food Items"])
        self.report_type.pack(side=tk.LEFT, padx=5)
        
        # Generate button
        ttk.Button(controls_frame, text="Generate Report", command=self.generate_report).pack(pady=10)
        
        # Report display area
        report_display_frame = ttk.Frame(content, padding=10, style='Card.TFrame')
        report_display_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.report_text = tk.Text(report_display_frame, height=15, wrap=tk.WORD)
        self.report_text.pack(fill=tk.BOTH, expand=True)
        
        # Set default values
        self.report_period.current(0)
        self.report_type.current(0)
    
    def show_profile(self):
        """Display the profile screen"""
        self.clear_frame()
        
        # Main container
        main_container = ttk.Frame(self.main_frame)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar
        sidebar = ttk.Frame(main_container, width=200, style='TFrame')
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Menu buttons
        menu_buttons = [
            ("Dashboard", self.show_dashboard),
            ("Food Database", self.show_food_database),
            ("Add Meal", self.show_add_meal),
            ("Daily Log", self.show_daily_log),
            ("Reports", self.show_reports),
            ("Profile", self.show_profile),
            ("Logout", self.logout)
        ]
        
        for text, command in menu_buttons:
            btn = ttk.Button(sidebar, text=text, command=command)
            btn.pack(fill=tk.X, pady=2)
        
        # Content area
        content = ttk.Frame(main_container)
        content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Profile title
        ttk.Label(content, text="Your Profile", 
                 style='Header.TLabel').pack(pady=10)
        
        # Profile form
        form_frame = ttk.Frame(content, padding=10, style='Card.TFrame')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Form fields
        fields = [
            ("Username:", None, self.current_user[1]),
            ("Email:", "profile_email", self.current_user[3]),
            ("Age:", "profile_age", self.current_user[4] if self.current_user[4] else ""),
            ("Weight (kg):", "profile_weight", self.current_user[5] if self.current_user[5] else ""),
            ("Height (cm):", "profile_height", self.current_user[6] if self.current_user[6] else ""),
            ("Gender:", "profile_gender", {"values": ["Male", "Female", "Other"], "value": self.current_user[7] if self.current_user[7] else ""}),
            ("Activity Level:", "profile_activity", {"values": ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"], "value": self.current_user[8] if self.current_user[8] else ""}),
            ("Goal:", "profile_goal", {"values": ["Weight Loss", "Weight Maintenance", "Weight Gain"], "value": self.current_user[9] if self.current_user[9] else ""}),
            ("Daily Calories:", "profile_calories", self.current_user[10] if self.current_user[10] else "")
        ]
        
        for i, (label_text, attr_name, field_value) in enumerate(fields):
            ttk.Label(form_frame, text=label_text).grid(row=i, column=0, padx=5, pady=5, sticky=tk.E)
            
            if attr_name is None:  # Readonly field (username)
                ttk.Label(form_frame, text=field_value).grid(row=i, column=1, padx=5, pady=5, sticky=tk.W)
            elif isinstance(field_value, dict):  # Combobox
                widget = ttk.Combobox(form_frame, width=25, **field_value)
                widget.grid(row=i, column=1, padx=5, pady=5, sticky=tk.W)
                setattr(self, attr_name, widget)
            else:  # Entry field
                widget = ttk.Entry(form_frame, width=25)
                widget.insert(0, field_value)
                widget.grid(row=i, column=1, padx=5, pady=5, sticky=tk.W)
                setattr(self, attr_name, widget)
        
        # Button frame
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Update Profile", command=self.update_profile).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Recalculate Calories", command=self.recalculate_calories, 
                  style='Secondary.TButton').pack(side=tk.LEFT, padx=5)
    
    # [All database operation methods remain exactly the same as in your original code]
    # Only the UI display methods have been modified for better interface
    
    def load_food_items(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT food_id, name, calories, protein, carbohydrates, fats, category 
                FROM food_items 
                WHERE user_id = %s OR user_id IS NULL
                ORDER BY name
            """, (self.current_user[0],))
            
            # Clear existing items
            for item in self.food_tree.get_children():
                self.food_tree.delete(item)
                
            # Add new items
            for food in cursor:
                self.food_tree.insert("", tk.END, values=food[1:], iid=food[0])
                
        except Error as e:
            messagebox.showerror("Error", f"Failed to load food items: {e}")
    
    def search_food(self):
        search_term = self.food_search_entry.get()
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT food_id, name, calories, protein, carbohydrates, fats, category 
                FROM food_items 
                WHERE (user_id = %s OR user_id IS NULL)
                AND name LIKE %s
                ORDER BY name
            """, (self.current_user[0], f"%{search_term}%"))
            
            # Clear existing items
            for item in self.food_tree.get_children():
                self.food_tree.delete(item)
                
            # Add new items
            for food in cursor:
                self.food_tree.insert("", tk.END, values=food[1:], iid=food[0])
                
        except Error as e:
            messagebox.showerror("Error", f"Failed to search food items: {e}")
    
    def save_food(self):
        # Get values from form
        name = self.food_name.get()
        calories = self.food_calories.get()
        protein = self.food_protein.get()
        carbs = self.food_carbs.get()
        fats = self.food_fats.get()
        category = self.food_category.get()
        serving = self.food_serving.get()
        
        # Validate required fields
        if not name or not calories:
            messagebox.showerror("Error", "Name and Calories are required fields")
            return
            
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO food_items 
                (name, calories, protein, carbohydrates, fats, category, serving_size, user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                name,
                float(calories),
                float(protein) if protein else 0,
                float(carbs) if carbs else 0,
                float(fats) if fats else 0,
                category if category else None,
                serving if serving else None,
                self.current_user[0]
            ))
            
            self.connection.commit()
            messagebox.showinfo("Success", "Food item saved successfully")
            self.show_food_database()
            
        except Error as e:
            messagebox.showerror("Error", f"Failed to save food item: {e}")
    
    def load_food_combobox(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT food_id, name 
                FROM food_items 
                WHERE user_id = %s OR user_id IS NULL
                ORDER BY name
            """, (self.current_user[0],))
            
            foods = cursor.fetchall()
            self.meal_food['values'] = [f"{f[0]} - {f[1]}" for f in foods]
            
        except Error as e:
            messagebox.showerror("Error", f"Failed to load food items: {e}")
    
    def add_food_to_meal(self):
        food_str = self.meal_food.get()
        quantity_str = self.meal_quantity.get()
        
        if not food_str or not quantity_str:
            messagebox.showerror("Error", "Please select a food and enter quantity")
            return
            
        try:
            quantity = float(quantity_str)
            if quantity <= 0:
                raise ValueError("Quantity must be positive")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive number for quantity")
            return
            
        try:
            food_id = int(food_str.split(" - ")[0])
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT name, calories 
                FROM food_items 
                WHERE food_id = %s
            """, (food_id,))
            
            food = cursor.fetchone()
            if food:
                # Convert Decimal to float for calculation
                calories_per_unit = float(food[1])
                total_calories = calories_per_unit * quantity
                
                self.meal_items_tree.insert("", tk.END, 
                                        values=(food[0], f"{calories_per_unit:.2f}", 
                                                f"{quantity:.2f}", f"{total_calories:.2f}"))
                self.meal_foods.append((food_id, quantity))
                
                # Update total calories
                current_total = sum(
                    float(self.meal_items_tree.item(item, 'values')[3]) 
                    for item in self.meal_items_tree.get_children()
                )
                self.meal_total_label.config(text=f"Total Calories: {current_total:.2f}")
                
        except (ValueError, Error) as e:
            messagebox.showerror("Error", f"Failed to add food to meal: {str(e)}")
    
    def save_meal(self):
        meal_type = self.meal_type.get()
        meal_date = self.meal_date.get()
        notes = self.meal_notes.get()
        
        if not meal_type or not meal_date:
            messagebox.showerror("Error", "Meal type and date are required")
            return
            
        if not self.meal_foods:
            messagebox.showerror("Error", "Please add at least one food item to the meal")
            return
            
        try:
            cursor = self.connection.cursor()
            
            # Save meal
            cursor.execute("""
                INSERT INTO meals (user_id, meal_type, date, notes)
                VALUES (%s, %s, %s, %s)
            """, (self.current_user[0], meal_type, meal_date, notes if notes else None))
            
            meal_id = cursor.lastrowid
            
            # Save meal items
            for food_id, quantity in self.meal_foods:
                cursor.execute("""
                    INSERT INTO meal_items (meal_id, food_id, quantity)
                    VALUES (%s, %s, %s)
                """, (meal_id, food_id, quantity))
            
            self.connection.commit()
            messagebox.showinfo("Success", "Meal saved successfully")
            self.show_dashboard()
            
        except Error as e:
            messagebox.showerror("Error", f"Failed to save meal: {e}")
    
    def load_daily_log(self):
        selected_date = self.log_date.get_date()
        
        try:
            cursor = self.connection.cursor()
            
            # Clear existing widgets
            for widget in self.log_summary_frame.winfo_children():
                widget.destroy()
                
            for widget in self.log_meals_frame.winfo_children():
                widget.destroy()
            
            # Get total calories for the day
            cursor.execute("""
                SELECT SUM(f.calories * mi.quantity)
                FROM meal_items mi
                JOIN food_items f ON mi.food_id = f.food_id
                JOIN meals m ON mi.meal_id = m.meal_id
                WHERE m.user_id = %s AND m.date = %s
            """, (self.current_user[0], selected_date))
            
            total_calories = cursor.fetchone()[0] or 0
            
            # Get goal calories
            goal_calories = self.current_user[10] or 2000
            
            # Display summary
            ttk.Label(self.log_summary_frame, 
                     text=f"Date: {selected_date} | Total Calories: {total_calories} / {goal_calories}",
                     font=('Segoe UI', 10)).pack(pady=5)
            
            progress = ttk.Progressbar(self.log_summary_frame, orient=tk.HORIZONTAL, 
                                     length=300, mode='determinate')
            progress.pack(pady=5)
            progress['value'] = min((total_calories / goal_calories) * 100, 100)
            
            # Get meals for the day
            cursor.execute("""
                SELECT m.meal_id, m.meal_type, m.notes
                FROM meals m
                WHERE m.user_id = %s AND m.date = %s
                ORDER BY m.meal_type
            """, (self.current_user[0], selected_date))
            
            meals = cursor.fetchall()
            
            if not meals:
                ttk.Label(self.log_meals_frame, text="No meals recorded for this day").pack(pady=10)
                return
                
            for meal in meals:
                meal_frame = ttk.Frame(self.log_meals_frame, padding=5, style='Card.TFrame')
                meal_frame.pack(fill=tk.X, pady=5, padx=5)
                
                # Meal header
                header_frame = ttk.Frame(meal_frame)
                header_frame.pack(fill=tk.X)
                
                ttk.Label(header_frame, text=meal[1], font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT)
                if meal[2]:
                    ttk.Label(header_frame, text=f"Notes: {meal[2]}").pack(side=tk.LEFT, padx=10)
                
                # Get meal items
                cursor.execute("""
                    SELECT f.name, f.calories, mi.quantity, (f.calories * mi.quantity) as total
                    FROM meal_items mi
                    JOIN food_items f ON mi.food_id = f.food_id
                    WHERE mi.meal_id = %s
                """, (meal[0],))
                
                items = cursor.fetchall()
                
                # Create treeview for meal items
                tree = ttk.Treeview(meal_frame, columns=("name", "calories", "quantity", "total"), show="headings")
                tree.heading("name", text="Food")
                tree.heading("calories", text="Calories per unit")
                tree.heading("quantity", text="Quantity")
                tree.heading("total", text="Total Calories")
                
                # Set column widths
                tree.column("name", width=200)
                tree.column("calories", width=120)
                tree.column("quantity", width=80)
                tree.column("total", width=100)
                
                meal_total = 0
                for item in items:
                    tree.insert("", tk.END, values=item)
                    meal_total += item[3]
                
                tree.pack(fill=tk.X, padx=5, pady=2)
                
                # Meal total
                ttk.Label(meal_frame, text=f"Meal Total: {meal_total} calories", 
                         font=('Segoe UI', 9, 'bold')).pack(side=tk.RIGHT, padx=5, pady=2)
                
        except Error as e:
            messagebox.showerror("Error", f"Failed to load daily log: {e}")
    
    def update_report_dates(self, event=None):
        if self.report_period.get() == "Custom":
            self.custom_date_frame.pack(fill=tk.X, pady=5)
        else:
            self.custom_date_frame.pack_forget()
    
    def generate_report(self):
        period = self.report_period.get()
        report_type = self.report_type.get()
        
        try:
            cursor = self.connection.cursor()
            
            # Determine date range
            if period == "Last 7 Days":
                end_date = date.today()
                start_date = end_date - timedelta(days=7)
            elif period == "Last 30 Days":
                end_date = date.today()
                start_date = end_date - timedelta(days=30)
            elif period == "This Month":
                today = date.today()
                start_date = date(today.year, today.month, 1)
                end_date = today
            else:  # Custom
                start_date = self.report_start_date.get_date()
                end_date = self.report_end_date.get_date()
            
            # Generate report based on type
            report_text = f"Report: {report_type}\nPeriod: {start_date} to {end_date}\n\n"
            
            if report_type == "Calorie Summary":
                cursor.execute("""
                    SELECT m.date, SUM(f.calories * mi.quantity) as daily_calories
                    FROM meal_items mi
                    JOIN food_items f ON mi.food_id = f.food_id
                    JOIN meals m ON mi.meal_id = m.meal_id
                    WHERE m.user_id = %s AND m.date BETWEEN %s AND %s
                    GROUP BY m.date
                    ORDER BY m.date
                """, (self.current_user[0], start_date, end_date))
                
                results = cursor.fetchall()
                
                if not results:
                    report_text += "No data available for the selected period."
                else:
                    report_text += "Daily Calorie Intake:\n"
                    report_text += "-" * 50 + "\n"
                    report_text += "Date\t\tCalories\tvs Goal\n"
                    report_text += "-" * 50 + "\n"
                    
                    goal = self.current_user[10] or 2000
                    total_calories = 0
                    days = 0
                    
                    for row in results:
                        date_str, calories = row
                        total_calories += calories
                        days += 1
                        vs_goal = "Under" if calories < goal else "Over" if calories > goal else "Met"
                        report_text += f"{date_str}\t{calories:.0f}\t\t{vs_goal}\n"
                    
                    avg_calories = total_calories / days if days > 0 else 0
                    report_text += "\n"
                    report_text += f"Average Daily Calories: {avg_calories:.0f}\n"
                    report_text += f"Goal: {goal}\n"
                    report_text += f"Average Difference: {avg_calories - goal:.0f}\n"
            
            elif report_type == "Macronutrients":
                cursor.execute("""
                    SELECT 
                        SUM(f.protein * mi.quantity) as total_protein,
                        SUM(f.carbohydrates * mi.quantity) as total_carbs,
                        SUM(f.fats * mi.quantity) as total_fats,
                        SUM(f.calories * mi.quantity) as total_calories
                    FROM meal_items mi
                    JOIN food_items f ON mi.food_id = f.food_id
                    JOIN meals m ON mi.meal_id = m.meal_id
                    WHERE m.user_id = %s AND m.date BETWEEN %s AND %s
                """, (self.current_user[0], start_date, end_date))
                
                result = cursor.fetchone()
                
                if not result or not result[3]:
                    report_text += "No data available for the selected period."
                else:
                    total_protein, total_carbs, total_fats, total_calories = result
                    
                    report_text += "Macronutrient Breakdown:\n"
                    report_text += "-" * 50 + "\n"
                    report_text += f"Total Calories: {total_calories:.0f}\n"
                    report_text += f"Protein: {total_protein:.0f}g ({(total_protein*4/total_calories)*100:.1f}%)\n"
                    report_text += f"Carbohydrates: {total_carbs:.0f}g ({(total_carbs*4/total_calories)*100:.1f}%)\n"
                    report_text += f"Fats: {total_fats:.0f}g ({(total_fats*9/total_calories)*100:.1f}%)\n"
            
            self.report_text.delete(1.0, tk.END)
            self.report_text.insert(tk.END, report_text)
            
        except Error as e:
            messagebox.showerror("Error", f"Failed to generate report: {e}")
    
    def update_profile(self):
        try:
            # Convert numeric fields with validation
            age = int(self.profile_age.get()) if self.profile_age.get() else None
            weight = float(self.profile_weight.get()) if self.profile_weight.get() else None
            height = float(self.profile_height.get()) if self.profile_height.get() else None
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for age, weight, and height")
            return

        email = self.profile_email.get()
        gender = self.profile_gender.get()
        activity = self.profile_activity.get()
        goal = self.profile_goal.get()
        calories = self.profile_calories.get()
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                UPDATE users SET
                email = %s,
                age = %s,
                weight = %s,
                height = %s,
                gender = %s,
                activity_level = %s,
                goal = %s,
                daily_calories = %s
                WHERE user_id = %s
            """, (
                email,
                age,
                weight,
                height,
                gender,
                activity,
                goal,
                int(calories) if calories else None,
                self.current_user[0]
            ))
            
            self.connection.commit()
            messagebox.showinfo("Success", "Profile updated successfully")
            
            # Refresh current user data
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (self.current_user[0],))
            self.current_user = cursor.fetchone()
            
        except Error as e:
            messagebox.showerror("Error", f"Failed to update profile: {e}")
    
    def recalculate_calories(self):
        age = self.profile_age.get()
        weight = self.profile_weight.get()
        height = self.profile_height.get()
        gender = self.profile_gender.get()
        activity = self.profile_activity.get()
        goal = self.profile_goal.get()
        
        if not all([age, weight, height, gender, activity, goal]):
            messagebox.showerror("Error", "Please fill in all fields to calculate calories")
            return
            
        try:
            daily_calories = self.calculate_daily_calories(
                int(age),
                float(weight),
                float(height),
                gender,
                activity,
                goal
            )
            
            self.profile_calories.delete(0, tk.END)
            self.profile_calories.insert(0, str(int(daily_calories)))
            messagebox.showinfo("Success", f"Calculated daily calories: {int(daily_calories)}")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for age, weight, and height")
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()
            
            if user:
                self.current_user = user
                self.show_dashboard()
            else:
                messagebox.showerror("Error", "Invalid username or password")
        except Error as e:
            messagebox.showerror("Error", f"Database error: {e}")
    
    def register(self):
        # Get all registration fields
        username = self.reg_username.get()
        password = self.reg_password.get()
        email = self.reg_email.get()
        
        # Validate required fields
        if not username or not password or not email:
            messagebox.showerror("Error", "Username, password, and email are required")
            return
        
        try:
            # Convert numeric fields with validation
            age = int(self.reg_age.get()) if self.reg_age.get() else None
            weight = float(self.reg_weight.get()) if self.reg_weight.get() else None
            height = float(self.reg_height.get()) if self.reg_height.get() else None
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for age, weight, and height")
            return

        gender = self.reg_gender.get()
        activity = self.reg_activity.get()
        goal = self.reg_goal.get()
        
        try:
            cursor = self.connection.cursor()
            
            # Check if username or email exists
            cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
            if cursor.fetchone():
                messagebox.showerror("Error", "Username or email already exists")
                return
            
            # Calculate daily calories
            daily_calories = self.calculate_daily_calories(
                age if age else 30,
                weight if weight else 70,
                height if height else 170,
                gender if gender else "Male",
                activity if activity else "Moderately Active",
                goal if goal else "Weight Maintenance"
            )
            
            # Insert new user
            cursor.execute("""
                INSERT INTO users (username, password, email, age, weight, height, gender, 
                                activity_level, goal, daily_calories)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                username, password, email,
                age, weight, height,
                gender, activity, goal,
                int(daily_calories)
            ))
            
            self.connection.commit()
            messagebox.showinfo("Success", "Registration successful! Please login.")
            self.show_login_screen()
        except Error as e:
            messagebox.showerror("Error", f"Database error: {e}")
    
    def calculate_daily_calories(self, age, weight, height, gender, activity, goal):
        # Harris-Benedict equation for BMR calculation
        if gender == "Male":
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        else:
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
        
        # Activity multiplier
        activity_multiplier = {
            "Sedentary": 1.2,
            "Lightly Active": 1.375,
            "Moderately Active": 1.55,
            "Very Active": 1.725,
            "Extremely Active": 1.9
        }.get(activity, 1.55)
        
        tdee = bmr * activity_multiplier
        
        # Goal adjustment
        if goal == "Weight Loss":
            return tdee * 0.85  # 15% deficit
        elif goal == "Weight Gain":
            return tdee * 1.15  # 15% surplus
        else:
            return tdee  # Maintenance
    
    def get_daily_calories(self, date):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT SUM(f.calories * m.quantity)
                FROM meal_items m
                JOIN food_items f ON m.food_id = f.food_id
                JOIN meals ml ON m.meal_id = ml.meal_id
                WHERE ml.user_id = %s AND ml.date = %s
            """, (self.current_user[0], date))
            
            result = cursor.fetchone()
            return float(result[0]) if result and result[0] else 0.0
        except Error as e:
            print(f"Error getting daily calories: {e}")
            return 0.0
    
    def get_recent_meals(self, limit=5):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT * FROM meals
                WHERE user_id = %s
                ORDER BY date DESC, meal_id DESC
                LIMIT %s
            """, (self.current_user[0], limit))
            
            return cursor.fetchall()
        except Error as e:
            print(f"Error getting recent meals: {e}")
            return []
    
    def get_meal_calories(self, meal_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT SUM(f.calories * m.quantity)
                FROM meal_items m
                JOIN food_items f ON m.food_id = f.food_id
                WHERE m.meal_id = %s
            """, (meal_id,))
            
            result = cursor.fetchone()
            return result[0] if result[0] else 0
        except Error as e:
            print(f"Error getting meal calories: {e}")
            return 0
    
    def logout(self):
        self.current_user = None
        self.show_login_screen()

if __name__ == "__main__":
    root = tk.Tk()
    app = DietManagementApp(root)
    root.mainloop()