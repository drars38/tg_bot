import sqlite3

DATABASE = 'support_bot.db'


async def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        phone_number TEXT
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        message_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        message TEXT,
        response TEXT,
        answered INTEGER DEFAULT 0,
        banned INTEGER DEFAULT 0,  
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS black_list (
        user_id INTEGER,
        message TEXT
    )
    ''')
    conn.commit()
    conn.close()


async def add_user(user_id, username, phone_number, full_name):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO users (user_id, username, phone_number, first_name) VALUES (?, ?, ?, ?)
    ''', (user_id, username, phone_number, full_name))
    conn.commit()
    conn.close()


async def get_first_name(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT first_name FROM users WHERE user_id = ?',
                   (user_id,))
    result = cursor.fetchall()
    conn.close()
    return result[0] if result else None


async def get_username(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT username FROM users WHERE user_id = ?',
                   (user_id,))
    result = cursor.fetchall()
    conn.close()
    return result[0] if result else None


async def add_message(user_id, message):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO messages (user_id, message) VALUES (?, ?)
    ''', (user_id, message))
    conn.commit()
    conn.close()


async def get_unanswered_messages():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT message_id, user_id, message FROM messages WHERE answered = 0 AND banned = 0
    ''')
    rows = cursor.fetchall()
    conn.close()
    return rows


async def respond_to_message(message_id, response):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE messages SET response = ?, answered = 1 WHERE message_id = ?
    ''', (response, message_id))
    conn.commit()
    conn.close()


async def get_respond(message_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT response FROM messages WHERE message_id = ?
    ''', (message_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows


async def get_chat_id(message_id, answered):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT user_id FROM messages WHERE message_id = ? AND answered = ?
    ''', (message_id, answered))
    row = cursor.fetchone()
    conn.close()
    return row


async def get_message(message_id, answered):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT message FROM messages WHERE message_id = ? AND answered = ?
    ''', (message_id, answered))
    row = cursor.fetchone()
    conn.close()
    return row


async def get_all_users():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()
    conn.close()
    return rows


async def check_user_or_registr(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row


async def get_history(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT message, response FROM messages WHERE user_id = ? AND answered = 1
    ''', (user_id,))
    row = cursor.fetchall()
    conn.close()
    return row


async def get_black_list():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM black_list')
    result = cursor.fetchall()
    conn.close()
    return [row[0] for row in result]


async def add_to_black_list(user_id, message):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO black_list (user_id, message) VALUES (?, ?)
    ''', (user_id, message))
    cursor.execute('''
    UPDATE messages SET banned = 1 WHERE user_id = ?
    ''', (user_id,))
    conn.commit()
    conn.close()


async def get_blocked_user_message(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT message FROM black_list WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


async def unban_user(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
    DELETE FROM black_list WHERE user_id = ?
    ''', (user_id,))
    cursor.execute('''
    UPDATE messages SET banned = 0 WHERE user_id = ?
    ''', (user_id,))
    conn.commit()
    conn.close()
