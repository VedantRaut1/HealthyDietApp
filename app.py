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
    password = "Vedant@12"  # Fixed Password
    
    register_user(name, age, weight, height, activity, goal, password)
    messagebox.showinfo("Success", "User Registered Successfully!")

def login():
    global current_user_id
    name = entry_login_name.get()
    password = "Vedant@12"  # Fixed Password
    
    user = login_user(name, password)
    
    if user:
        current_user_id = user[0]
        messagebox.showinfo("Login Successful", f"Welcome {name}!")
    else:
        messagebox.showerror("Error", "Invalid Credentials")

def add_diet_entry():
    if current_user_id is None:
        messagebox.showerror("Error", "Please login first!")
        return
    
    add_diet(current_user_id, entry_calories.get(), entry_protein.get(), entry_carbs.get(), entry_fat.get(), entry_meal_type.get())
    messagebox.showinfo("Success", "Diet Plan Added!")

def add_food_entry():
    if current_user_id is None:
        messagebox.showerror("Error", "Please login first!")
        return
    
    add_food_log(current_user_id, entry_date.get(), entry_meal.get(), entry_food.get(), entry_food_calories.get())
    messagebox.showinfo("Success", "Food Logged!")

def show_calories():
    if current_user_id is None:
        messagebox.showerror("Error", "Please login first!")
        return
    
    total_calories = get_caloric_summary(current_user_id)
    messagebox.showinfo("Caloric Summary", f"Total Calories Consumed: {total_calories}")

# Initialize Tkinter window
root = tk.Tk()
root.title("Healthy Diet Management")
root.geometry("400x500")

# Login UI
tk.Label(root, text="Login", font=("Arial", 16)).pack()
tk.Label(root, text="Username:").pack()
entry_login_name = tk.Entry(root)
entry_login_name.pack()

tk.Label(root, text="Password:").pack()
entry_login_password = tk.Entry(root, show="*")
entry_login_password.pack()

tk.Button(root, text="Login", command=login).pack(pady=10)

# Registration UI
tk.Label(root, text="Register", font=("Arial", 16)).pack()

entry_name = tk.Entry(root)
entry_name.pack()
add_placeholder(entry_name, "Name")

entry_age = tk.Entry(root)
entry_age.pack()
add_placeholder(entry_age, "Age")

entry_weight = tk.Entry(root)
entry_weight.pack()
add_placeholder(entry_weight, "Weight")

entry_height = tk.Entry(root)
entry_height.pack()
add_placeholder(entry_height, "Height")

entry_activity = tk.Entry(root)
entry_activity.pack()
add_placeholder(entry_activity, "Activity Level")

entry_goal = tk.Entry(root)
entry_goal.pack()
add_placeholder(entry_goal, "Goal")

entry_password = tk.Entry(root, show="*")
entry_password.pack()

tk.Button(root, text="Register", command=register).pack(pady=10)

root.mainloop()
