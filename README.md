# Secure-Password-Storage

You are auditing the authentication module of a Python-based Security Portal. The provided application (app.py) currently hashes user passwords using the MD5 algorithm.

This contains a critical security flaw. MD5 is a severely outdated hashing algorithm designed to be extremely fast, which makes it highly vulnerable to brute-force and "rainbow table" attacks. Modern systems must use intentionally slow algorithms like bcrypt, which automatically append a random "salt" to every password, neutralizing these attacks entirely.

Furthermore, as a Security Engineer, you cannot simply flip a switch to update the algorithm, as that would immediately invalidate every existing user's password. You must architect a Seamless Legacy Migration, where old users are securely upgraded in the background the next time they successfully log in.

Project Structure:
You are given a few key files:

setup_users.py: A script to initialize a fresh, empty local SQLite database (users.db).
app.py: The interactive CLI backend containing the vulnerable signup route and incomplete login logic.
Your Task
Observe the vulnerable state of the database. Then, act as the defender and patch app.py by integrating the bcrypt library to secure new signups, verify modern hashes, and silently upgrade legacy accounts.

Phase 1: The Vulnerability

Open your terminal and initialize the database with the legacy user by running: python setup_users.py
Install the required cryptographic library by executing below command in your terminal:
pip install bcrypt
Start the interactive application by running: python app.py
Type 3 and press Enter to select View Database (Admin). Look at the database: alice has a short, 32-character MD5 hash.
Type 1 to Signup a new user (e.g., Username: bob, Password: secure123).
Type 3 to view the database again. Notice that bob was also registered using a vulnerable MD5 hash! The system is actively creating weak credentials.
Type 4 to exit the application.
Docs: OWASP Password Storage Cheat Sheet
Phase 2: The Defense

Open app.py in your code editor.
TODO 1 (Secure Signup): Delete the vulnerable MD5 hashing logic. Instead, implement the bcrypt library to securely hash the user's password with a dynamically generated salt. Remember that bcrypt requires byte strings, so you will need to encode the password before hashing and decode the result before storing it in the database. (Hint: The exact syntax looks like this: bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()).
TODO 2 (Verify Modern Hashes): Inside the login function, verify if the retrieved hash is a modern bcrypt hash (they universally begin with the $2 prefix). If it is, use the bcrypt library's secure comparison function to check if the user's input matches the stored database hash. Don't forget to encode both strings into bytes for the comparison to work. (Hint: The exact syntax looks like this: bcrypt.checkpw(password_input.encode(), stored_hash.encode())).
TODO 3 (Background Migration): Under the else block, the system successfully verifies legacy MD5 users. Below the print("Legacy MD5 hash detected...") statement, write the code to hash their plain-text password using bcrypt, and then execute an SQL UPDATE statement to overwrite their old MD5 hash in the database with the new secure one. and then commit the database changes.
Docs: Bcrypt Library
Expected Behaviour:

Phase 1: Before Patching (The Vulnerable State)
Users are given short, highly crackable MD5 hashes.
USERNAME     | PASSWORD HASH
---------------------------------------------------------------------------
alice        | 6384e2b2184bcbf58eccf10ca7a6563c
bob          | 9f9d51bc70ef21ca5c14f307980a29d8
---------------------------------------------------------------------------
Phase 2: After Patching (The Successful Defense & Migration)
New users are given secure hashes. When you log in as alice (Password: password123), the system silently upgrades her password hash in the background. Viewing the database confirms all hashes now begin with the secure $2b$ prefix.
USERNAME     | PASSWORD HASH
---------------------------------------------------------------------------
alice        | $2b$12$v9y3GtX9HVeDdV3A22T7wOvOO.pjeubn/znhLrkS1hnA6NRQsD8c6
bob          | $2b$12$UKoDQHk2k2YK0U8WZ.o5buqT5Zy7WACaI0pGd7L8G0cmBvCGvVDuS
---------------------------------------------------------------------------
Did you like the problem?
1 user found this helpful
