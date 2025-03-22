import tkinter as tk
from tkinter import messagebox
from diet_queries import register_user, login_user, add_diet, add_food_log, get_caloric_summary

current_user_id = None

# Function to add placeholders
def add_placeholder(entry, text):
    entry.insert(0, text)
    entry.config(fg="gray")
    
    def on_focus_in(event):
        if entry.get() == text:
            entry.delete(0, tk.END)
            entry.config(fg="black")
    
    def on_focus_out(event):
        if not entry.get():
            add_placeholder(entry, text)
    
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

def register():
    name = entry_name.get()
    age = entry_age.get()
    weight = entry_weight.get()
    height = entry_height.get()
    activity = entry_activity.get()
    goal = entry_goal.get()
    password = entry_password.get()  # Use the actual password input
    
    register_user(name, age, weight, height, activity, goal, password)
    messagebox.showinfo("Success", "User Registered Successfully!")

def login():
    global current_user_id
    name = entry_login_name.get()
    password = entry_login_password.get()  # Use the actual password input
    
    user = login_user(name, password)
    
    if user:
        current_user_id = user[0]
        messagebox.showinfo("Login Successful", f"Welcome {name}!")
        show_main_frame()  # Show the main app after login
    else:
        messagebox.showerror("Error", "Invalid Credentials")

def add_diet_entry():
    if current_user_id is None:
        messagebox.showerror("Error", "Please login first!")
        return
    
    add_diet(
        current_user_id, 
        entry_calories.get(), 
        entry_protein.get(), 
        entry_carbs.get(), 
        entry_fat.get(), 
        entry_meal_type.get()
    )
    messagebox.showinfo("Success", "Diet Plan Added!")

def add_food_entry():
    if current_user_id is None:
        messagebox.showerror("Error", "Please login first!")
        return
    
    add_food_log(
        current_user_id, 
        entry_date.get(), 
        entry_meal.get(), 
        entry_food.get(), 
        entry_food_calories.get()
    )
    messagebox.showinfo("Success", "Food Logged!")

def show_calories():
    if current_user_id is None:
        messagebox.showerror("Error", "Please login first!")
        return
    
    total_calories = get_caloric_summary(current_user_id)
    messagebox.showinfo("Caloric Summary", f"Total Calories Consumed: {total_calories}")

def show_main_frame():
    login_frame.pack_forget()
    register_frame.pack_forget()
    main_frame.pack(fill=tk.BOTH, expand=True)

def show_login_frame():
    main_frame.pack_forget()
    register_frame.pack_forget()
    login_frame.pack(fill=tk.BOTH, expand=True)

def show_register_frame():
    main_frame.pack_forget()
    login_frame.pack_forget()
    register_frame.pack(fill=tk.BOTH, expand=True)

# Initialize Tkinter window
root = tk.Tk()
root.title("Healthy Diet Management")
root.geometry("400x600")

# Create frames for different sections
login_frame = tk.Frame(root)
register_frame = tk.Frame(root)
main_frame = tk.Frame(root)

# Login Frame
tk.Label(login_frame, text="Login", font=("Arial", 16)).pack(pady=10)
tk.Label(login_frame, text="Username:").pack()
entry_login_name = tk.Entry(login_frame)
entry_login_name.pack(pady=5)
tk.Label(login_frame, text="Password:").pack()
entry_login_password = tk.Entry(login_frame, show="*")
entry_login_password.pack(pady=5)
tk.Button(login_frame, text="Login", command=login).pack(pady=10)
tk.Button(login_frame, text="New User? Register", command=show_register_frame).pack()

# Registration Frame
tk.Label(register_frame, text="Register", font=("Arial", 16)).pack(pady=10)

entry_name = tk.Entry(register_frame)
entry_name.pack(pady=5)
add_placeholder(entry_name, "Name")

entry_age = tk.Entry(register_frame)
entry_age.pack(pady=5)
add_placeholder(entry_age, "Age")

entry_weight = tk.Entry(register_frame)
entry_weight.pack(pady=5)
add_placeholder(entry_weight, "Weight")

entry_height = tk.Entry(register_frame)
entry_height.pack(pady=5)
add_placeholder(entry_height, "Height")

entry_activity = tk.Entry(register_frame)
entry_activity.pack(pady=5)
add_placeholder(entry_activity, "Activity Level")

entry_goal = tk.Entry(register_frame)
entry_goal.pack(pady=5)
add_placeholder(entry_goal, "Goal")

entry_password = tk.Entry(register_frame, show="*")
entry_password.pack(pady=5)
add_placeholder(entry_password, "Password")

tk.Button(register_frame, text="Register", command=register).pack(pady=10)
tk.Button(register_frame, text="Already have an account? Login", command=show_login_frame).pack()

# Main Application Frame (after login)
tk.Label(main_frame, text="Healthy Diet Management", font=("Arial", 16)).pack(pady=10)

# Diet Entry Section
tk.Label(main_frame, text="Add Diet Plan", font=("Arial", 12)).pack(pady=5)
tk.Frame(main_frame, height=1, bg="gray").pack(fill=tk.X, padx=20, pady=5)

entry_calories = tk.Entry(main_frame)
entry_calories.pack(pady=5)
add_placeholder(entry_calories, "Calories")

entry_protein = tk.Entry(main_frame)
entry_protein.pack(pady=5)
add_placeholder(entry_protein, "Protein (g)")

entry_carbs = tk.Entry(main_frame)
entry_carbs.pack(pady=5)
add_placeholder(entry_carbs, "Carbs (g)")

entry_fat = tk.Entry(main_frame)
entry_fat.pack(pady=5)
add_placeholder(entry_fat, "Fat (g)")

entry_meal_type = tk.Entry(main_frame)
entry_meal_type.pack(pady=5)
add_placeholder(entry_meal_type, "Meal Type")

tk.Button(main_frame, text="Add Diet Plan", command=add_diet_entry).pack(pady=10)

# Food Log Section
tk.Label(main_frame, text="Log Food", font=("Arial", 12)).pack(pady=5)
tk.Frame(main_frame, height=1, bg="gray").pack(fill=tk.X, padx=20, pady=5)

entry_date = tk.Entry(main_frame)
entry_date.pack(pady=5)
add_placeholder(entry_date, "Date (YYYY-MM-DD)")

entry_meal = tk.Entry(main_frame)
entry_meal.pack(pady=5)
add_placeholder(entry_meal, "Meal Name")

entry_food = tk.Entry(main_frame)
entry_food.pack(pady=5)
add_placeholder(entry_food, "Food Item")

entry_food_calories = tk.Entry(main_frame)
entry_food_calories.pack(pady=5)
add_placeholder(entry_food_calories, "Calories")

tk.Button(main_frame, text="Log Food", command=add_food_entry).pack(pady=10)

# Summary Button
tk.Button(main_frame, text="Show Caloric Summary", command=show_calories).pack(pady=10)

# Show the login frame initially
show_login_frame()

# Start the application
root.mainloop()
