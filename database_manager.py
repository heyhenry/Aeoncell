import sqlite3
import argon2

class DatabaseManager:
    def __init__(self):
        self.db = "aeoncell_database.db"
        self.ph = argon2.PasswordHasher()
        self.db_connection = sqlite3.connect(self.db)
        self.db_cursor = self.db_connection.cursor()
        self.create_authentication_table()
        self.create_profile_table()
        self.create_exercise_table()
        self.create_steps_table()
        self.create_hydration_table()
        self.create_sleep_table()
        self.db_connection.commit()

    def create_authentication_table(self):
        self.db_cursor.execute("CREATE TABLE IF NOT EXISTS authentication (username TEXT, hashed_password TEXT)")

    def create_username_and_password(self, username, password):
        hashed_password = self.ph.hash(password)
        self.db_cursor.execute("INSERT INTO authentication (username, hashed_password) values (?, ?)", (username, hashed_password))
        # create the initial profile details and store the given username
        self.db_cursor.execute("INSERT INTO profile_details (username) values (?)", (username,))
        self.db_connection.commit()

    def verify_password(self, given_password):
        self.db_cursor.execute("SELECT hashed_password FROM authentication WHERE rowid=1")
        result = self.db_cursor.fetchone()
        hashed_password = result[0]

        try:
            self.ph.verify(hashed_password, given_password)
            return True
        except argon2.exceptions.VerifyMismatchError:
            return False
        
    def check_password_exists(self):
        self.db_cursor.execute("SELECT hashed_password FROM authentication WHERE rowid = 1")
        if self.db_cursor.fetchone():
            return True
        
    def create_exercise_table(self):
        create_exercise_table_query = """
        CREATE TABLE IF NOT EXISTS exercise_entries (
            id INTEGER PRIMARY KEY,
            entry_type TEXT NOT NULL,
            exercise_label TEXT,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            exercise_name TEXT NOT NULL,
            sets_count INTEGER NOT NULL,
            reps_count INTEGER NOT NULL,
            weight_value INTEGER NOT NULL
        )
        """
        self.db_cursor.execute(create_exercise_table_query)

    def create_steps_table(self):
        create_steps_table_query = """
        CREATE TABLE IF NOT EXISTS steps_tracker (
            id INTEGER PRIMARY KEY,
            date TEXT NOT NULL,
            steps_taken INTEGER
        )
        """
        self.db_cursor.execute(create_steps_table_query)

    def create_hydration_table(self):
        create_hydration_table_query = """
        CREATE TABLE IF NOT EXISTS hydration_tracker (
            id INTEGER PRIMARY KEY,
            date TEXT NOT NULL,
            consumption_ml FLOAT
        )
        """
        self.db_cursor.execute(create_hydration_table_query)

    def create_sleep_table(self):
        create_sleep_table_query = """
        CREATE TABLE IF NOT EXISTS sleep_tracker (
            id INTEGER PRIMARY KEY,
            date TEXT NOT NULL,
            sleep_hrs FLOAT
        )
        """
        self.db_cursor.execute(create_sleep_table_query)

    def create_profile_table(self):
        create_profile_table_query = """
        CREATE TABLE IF NOT EXISTS profile_details (
            username TEXT NOT NULL,
            first_name TEXT,
            last_name TEXT,
            age INTEGER,
            height INTEGER,
            current_weight INTEGER,
            goal_weight INTEGER,
            daily_sleep_goal FLOAT,
            daily_steps_goal INTEGER,
            daily_hydration_goal FLOAT,
            monthly_weight_goal INTEGER,
            monthly_hydration_goal FLOAT,
            monthly_sleep_goal FLOAT,
            monthly_steps_goal INTEGER
        )
        """
        self.db_cursor.execute(create_profile_table_query)