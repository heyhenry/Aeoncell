import sqlite3

connection = sqlite3.connect("exercise_logs.db")
cursor = connection.cursor()

create_table = """
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
cursor.execute(create_table)

dummy_sample = """
INSERT INTO exercise_entries (
type,
label,
date, 
time,
exercise_name,
sets, 
reps,
weight
) VALUES ('single', '', '22/04/2025', '10:00', 'Bench Press', 5, 3, '60kg')
"""
cursor.execute(dummy_sample)

dummy_sample = """
INSERT INTO exercise_entries (
type,
label,
date, 
time,
exercise_name,
sets, 
reps,
weight
) VALUES ('session', '', '24/04/2025', '12:00', 'Bench Press', 5, 3, '60kg')
"""
cursor.execute(dummy_sample)

dummy_sample = """
INSERT INTO exercise_entries (
type,
label,
date, 
time,
exercise_name,
sets, 
reps,
weight
) VALUES ('session', '', '24/04/2025', '12:00', 'Triceps Pressdowns', 5, 3, '10kg')
"""
cursor.execute(dummy_sample)

dummy_sample = """
INSERT INTO exercise_entries (
type,
label,
date, 
time,
exercise_name,
sets, 
reps,
weight
) VALUES ('session', '', '24/04/2025', '12:00', 'Inclined Bench Press', 5, 3, '40kg')
"""
cursor.execute(dummy_sample)

connection.commit()

show_session = """
SELECT * FROM exercise_entries WHERE type = 'session' AND date = '22/04/2025'
"""
cursor.execute(show_session)
for i in cursor.fetchall():
    print(i)