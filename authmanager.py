import sqlite3
import argon2
import os
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode

class AuthManager:
    def __init__(self):
        self.auth_db = "authentication.db"
        self.ph = argon2.PasswordHasher()
        self.auth_connection = sqlite3.connect(self.auth_db)
        self.auth_cursor = self.auth_connection.cursor()

    def create_auth_database(self):
        self.auth_cursor.execute("CREATE TABLE IF NOT EXISTS authentication (desc TEXT, hash TEXT)")

    def create_password(self, password):
        self.create_auth_database()
        hashed_password = self.ph.hash(password)
        self.auth_cursor.execute("INSERT INTO authentication (desc, hash) values ('password', ?)", (hashed_password,))
        self.auth_connection.commit()

    def verify_password(self, given_password):
        self.auth_cursor.execute("SELECT hash FROM authentication WHERE rowid=1")
        result = self.auth_cursor.fetchone()
        hashed_password = result[0]

        try:
            self.ph.verify(hashed_password, given_password)
            return True
        except argon2.exceptions.VerifyMismatchError:
            return False
        
    def check_password_exists(self):
        self.auth_cursor.execute("SELECT hash FROM authentication WHERE rowid = 1")
        if self.auth_cursor.fetchone():
            return True