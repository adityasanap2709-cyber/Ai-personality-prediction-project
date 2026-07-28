import sqlite3

# Database Connection
connection = sqlite3.connect("database.db")
cursor = connection.cursor()

# ================= PREDICTIONS TABLE =================
cursor.execute("""
CREATE TABLE IF NOT EXISTS predictions (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT NOT NULL,
    user_id INTEGER NOT NULL,

    personality_type TEXT NOT NULL,

    confidence INTEGER NOT NULL,

    introvert INTEGER,

    thinking INTEGER,

    judging INTEGER,

    intuition INTEGER,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")

# ================= USERS TABLE =================
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT NOT NULL,

    email TEXT UNIQUE NOT NULL,

    password TEXT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")

connection.commit()
connection.close()

print("✅ Database Created Successfully!")