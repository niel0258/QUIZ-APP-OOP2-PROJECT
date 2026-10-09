
import os
import sqlite3
import hashlib
import hmac
import secrets

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.db")


def get_connection():
    """Return a connection to users.db."""
    return sqlite3.connect(DB_PATH)

DEFAULT_TEACHER = ("teacher", "teacher123")


def _hash_password(password, salt=None):
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 200_000).hex()
    return f"{salt}${digest}"


def initialize_storage():
    """Create the users table and a default teacher account if no users exist."""
    conn = get_connection()
    try:
        with conn:
            conn.execute(
                """CREATE TABLE IF NOT EXISTS users (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       username TEXT NOT NULL UNIQUE,
                       password_hash TEXT NOT NULL,
                       role TEXT NOT NULL
                   )"""
            )
            if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
                conn.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                             (DEFAULT_TEACHER[0], _hash_password(DEFAULT_TEACHER[1]), "Teacher"))
    finally:
        conn.close()


def create_user(username, password, role="Student"):
    """Create an account. Returns True on success, False if the username is taken."""
    conn = get_connection()
    try:
        with conn:
            conn.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                         (username, _hash_password(password), role))
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def verify_user(username, password):
    """Return the user's role if the credentials are valid, otherwise None."""
    conn = get_connection()
    try:
        row = conn.execute("SELECT password_hash, role FROM users WHERE username = ?", (username,)).fetchone()
    finally:
        conn.close()
    if not row:
        return None
    salt = row[0].split("$")[0]
    if hmac.compare_digest(_hash_password(password, salt), row[0]):
        return row[1]
    return None
