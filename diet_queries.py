import mysql.connector

# ✅ Establish Database Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Vedant@12",  # Root password updated
    database="healthy_diet"
)

cursor = conn.cursor()

# ✅ Function to Register a User
def register_user(name, age, weight, height, activity, goal, password):
    query = "INSERT INTO users (name, age, weight, height, activity_level, goal, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (name, age, weight, height, activity, goal, password)
    cursor.execute(query, values)
    conn.commit()

# ✅ Function to Login a User
def login_user(name, password):
    query = "SELECT id FROM users WHERE name = %s AND password = %s"
    cursor.execute(query, (name, password))
    return cursor.fetchone()

# ✅ Function to Add Diet Entry
def add_diet(user_id, calories, protein, carbs, fat, meal_type):
    query = "INSERT INTO diet (user_id, calories, protein, carbs, fat, meal_type) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (user_id, calories, protein, carbs, fat, meal_type)
    cursor.execute(query, values)
    conn.commit()

# ✅ Function to Add Food Log
def add_food_log(user_id, date, meal, food, food_calories):
    query = "INSERT INTO food_log (user_id, date, meal, food, food_calories) VALUES (%s, %s, %s, %s, %s)"
    values = (user_id, date, meal, food, food_calories)
    cursor.execute(query, values)
    conn.commit()

# ✅ Function to Get Total Calories
def get_caloric_summary(user_id):
    query = "SELECT SUM(food_calories) FROM food_log WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    return cursor.fetchone()[0] or 0
