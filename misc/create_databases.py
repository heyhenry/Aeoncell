import sqlite3

connection = sqlite3.connect("aeoncell_database.db")
cursor = connection.cursor()

create_exercise_table = """
CREATE TABLE IF NOT EXISTS exercise_entries (
id INTEGER PRIMARY KEY,
type TEXT NOT NULL,
label TEXT, 
date TEXT NOT NULL,
time TEXT NOT NULL,
exercise_name TEXT NOT NULL,
sets INTEGER,
reps INTEGER,
weight TEXT
)
"""
cursor.execute(create_exercise_table)

create_steps_table = """
CREATE TABLE IF NOT EXISTS steps_tracker (
id INTEGER PRIMARY KEY,
date TEXT NOT NULL,
total_steps INTEGER
)
"""
cursor.execute(create_steps_table)

connection.commit()