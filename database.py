import sqlite3
import json
import os

DB_FILE = "automation.db"

# ---------------------------------------------------------
# AUTO INITIALIZE DATABASE
# ---------------------------------------------------------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # User table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    # Config table
    c.execute("""
        CREATE TABLE IF NOT EXISTS configs (
            user_id INTEGER UNIQUE,
            chat_id TEXT,
            chat_type TEXT,
            delay INTEGER,
            cookies TEXT,
            messages TEXT,
            running INTEGER DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()

# Run DB init once
init_db()

# ---------------------------------------------------------
# USER MANAGEMENT
# ---------------------------------------------------------
def create_user(username, password):
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()

        c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                  (username, password))
        conn.commit()
        conn.close()

        return True, "User created successfully."

    except Exception as e:
        return False, str(e)


def verify_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("SELECT id FROM users WHERE username=? AND password=?",
              (username, password))
    row = c.fetchone()

    conn.close()

    return row[0] if row else None


# ---------------------------------------------------------
# CONFIG SAVE / LOAD
# ---------------------------------------------------------
def get_user_config(user_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("SELECT chat_id, chat_type, delay, cookies, messages, running FROM configs WHERE user_id=?",
              (user_id,))
    row = c.fetchone()

    conn.close()

    if not row:
        return {
            "chat_id": "",
            "chat_type": "E2EE",
            "delay": 15,
            "cookies": "",
            "messages": "",
            "running": False
        }

    return {
        "chat_id": row[0],
        "chat_type": row[1],
        "delay": row[2],
        "cookies": row[3],
        "messages": row[4],
        "running": bool(row[5])
    }


def update_user_config(user_id, chat_id, chat_type, delay, cookies, messages, running=False):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Check if config exists
    c.execute("SELECT user_id FROM configs WHERE user_id=?", (user_id,))
    exists = c.fetchone()

    if exists:
        c.execute("""
            UPDATE configs
            SET chat_id=?, chat_type=?, delay=?, cookies=?, messages=?, running=?
            WHERE user_id=?
        """, (chat_id, chat_type, delay, cookies, messages, int(running), user_id))
    else:
        c.execute("""
            INSERT INTO configs (user_id, chat_id, chat_type, delay, cookies, messages, running)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, chat_id, chat_type, delay, cookies, messages, int(running)))

    conn.commit()
    conn.close()
    return True
