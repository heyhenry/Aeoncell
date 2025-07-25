import sqlite3
from utils import achievement_map

db_connection = sqlite3.connect("aeoncell_database.db")
db_cursor = db_connection.cursor()

achievement_names = {
    i : ""
    for i in range(1, 5)
}
achievement_badges = {
    i : "Badge Goes Here"
    for i in range(1, 5)
}
achievement_unlock_dates = {
    i : ""
    for i in range(1, 5)
}

db_cursor.execute("SELECT achievement_id, achievement_unlock_date FROM achievements_details ORDER BY achievement_unlock_date DESC LIMIT 4")
results = db_cursor.fetchall()

for i in range(len(results)):
    if results[i][1] == "":
        continue
    achievement_names[i+1] = achievement_map.achievement_lookup[results[i][0]][1]
    achievement_badges[i+1] = f"achievement: {results[i][0]} badge here"
    achievement_unlock_dates[i+1] = results[i][1]

for i in range(1, 5):
    print(f"==========[Badge Slot {i}]==========")
    print(f"Achievement Name: {achievement_names[i]}")
    print(f"Achievement Badge: {achievement_badges[i]}")
    print(f"Achievement Unlock Date: {achievement_unlock_dates[i]}")
    print("=====================================\n")

