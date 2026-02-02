# Example: SQL Injection Vulnerability
# Run: sentinel apply examples/vulnerable_sql.py

import sqlite3

def get_user(username):
    """
    VULNERABLE: This function is susceptible to SQL Injection.
    An attacker can input: ' OR '1'='1
    """
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    # BAD: String concatenation in SQL query
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    
    return cursor.fetchone()

if __name__ == "__main__":
    # Test with safe input
    print(get_user("alice"))
    
    # Attacker input would be: ' OR '1'='1
