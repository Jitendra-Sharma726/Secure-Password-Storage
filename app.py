import hashlib
import bcrypt
import sqlite3

DB_FILE = 'users.db'

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    return conn

def signup():
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    
    # VULNERABILITY: New users are still being registered with MD5.
    # TODO 1: Delete the MD5 line below. Use the bcrypt library to securely 
    # hash the password with a generated salt, and decode it to a string.
    hashed = hashlib.md5(password.encode()).hexdigest()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
        conn.commit()
        print(f"User '{username}' registered successfully.")
    except sqlite3.IntegrityError:
        print("Error: Username already exists.")
    finally:
        conn.close()

def login():
    username = input("Username: ").strip()
    password_input = input("Password: ").strip()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    
    if not row:
        print("Login failed: Invalid credentials.")
        conn.close()
        return
        
    stored_hash = row[0]
    
    # Check if the stored hash is a modern bcrypt hash (they always start with $2b$)
    if stored_hash.startswith('$2b$'):
        # TODO 2: The user has a modern hash! Use bcrypt.checkpw() to verify 
        # their password_input against the stored_hash.
        print("TODO: Implement bcrypt verification here.")
        
    else:
        # The stored hash does not start with $2b$, so it must be a legacy MD5 hash.
        md5_input = hashlib.md5(password_input.encode()).hexdigest()
        
        if md5_input == stored_hash:
            print("Login successful! 🎉")
            print("Legacy MD5 hash detected. Initiating background migration...")
            
            # VULNERABILITY: We are letting them log in, but we aren't upgrading their security.
            # TODO 3: The user has provided their correct plain-text password. 
            # Hash this password using bcrypt, then execute an SQL UPDATE statement 
            # to replace their old MD5 hash in the database with the new secure hash.
            
        else:
            print("Login failed: Invalid credentials.")
            
    conn.close()

def view_database():
    """Helper function to let students see the database state in real-time."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, password FROM users")
    users = cursor.fetchall()
    
    print(f"\n{'USERNAME':<12} | {'PASSWORD HASH'}")
    print("-" * 75)
    
    if not users:
        print("The database is currently empty.")
    else:
        for user in users:
            print(f"{user[0]:<12} | {user[1]}")
            
    print("-" * 75)
    conn.close()

if __name__ == "__main__":
    print("=== Security Portal ===")
    
    while True:
        print("\n1. Signup")
        print("2. Login")
        print("3. View Database (Admin)")
        print("4. Exit")
        choice = input("Select an option (1/2/3/4): ").strip()
        
        if choice == '1':
            print("\n--- Signup ---")
            signup()
        elif choice == '2':
            print("\n--- Login ---")
            login()
        elif choice == '3':
            view_database()
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid selection.")


