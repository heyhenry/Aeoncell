import sqlite3
from utils import achievement_map
import customtkinter as ctk
from pages.images import achievement_images

db_connection = sqlite3.connect("aeoncell_database.db")
db_cursor = db_connection.cursor()




root = ctk.CTk()

achievement_names = {
    i : ctk.StringVar(value="Name Pending")
    for i in range(1, 5)
}
achievement_badges = {
    i : achievement_images.loading_achievement_icon
    for i in range(1, 5)
}
achievement_unlock_dates = {
    i : ctk.StringVar(value="Date Pending")
    for i in range(1, 5)
}

def update_latest_achievements_display():
    db_cursor.execute("SELECT achievement_id, achievement_unlock_date FROM achievements_details ORDER BY achievement_unlock_date DESC LIMIT 4")
    results = db_cursor.fetchall()

    for i in range(len(results)):
        if results[i][1] == "":
            continue
        achievement_names[i+1].set(achievement_map.achievement_lookup[results[i][0]][1])
        achievement_badges[i+1] = achievement_images.unlocked_achievements[results[i][0]]
        achievement_unlock_dates[i+1].set(results[i][1])

    # for i in range(1, 5):
    #     print(f"==========[Badge Slot {i}]==========")
    #     print(f"Achievement Name: {achievement_names[i]}")
    #     print(f"Achievement Badge: {achievement_badges[i]}")
    #     print(f"Achievement Unlock Date: {achievement_unlock_dates[i]}")
    #     print("=====================================\n")

update_latest_achievements_display()

badge_1_frame = ctk.CTkFrame(root)
badge_1_name = ctk.CTkLabel(badge_1_frame, textvariable=achievement_names[1])
badge_1_icon = ctk.CTkLabel(badge_1_frame, text="", image=achievement_badges[1])
badge_1_date = ctk.CTkLabel(badge_1_frame, textvariable=achievement_unlock_dates[1])

badge_1_frame.grid(row=0, column=0)
badge_1_name.grid(row=0, column=0)
badge_1_icon.grid(row=1, column=0)
badge_1_date.grid(row=2, column=0)

badge_2_frame = ctk.CTkFrame(root)
badge_2_name = ctk.CTkLabel(badge_2_frame, textvariable=achievement_names[2])
badge_2_icon = ctk.CTkLabel(badge_2_frame, text="", image=achievement_badges[2])
badge_2_date = ctk.CTkLabel(badge_2_frame, textvariable=achievement_unlock_dates[2])

badge_2_frame.grid(row=0, column=1)
badge_2_name.grid(row=0, column=0)
badge_2_icon.grid(row=1, column=0)
badge_2_date.grid(row=2, column=0)

badge_3_frame = ctk.CTkFrame(root)
badge_3_name = ctk.CTkLabel(badge_3_frame, textvariable=achievement_names[3])
badge_3_icon = ctk.CTkLabel(badge_3_frame, text="", image=achievement_badges[3])
badge_3_date = ctk.CTkLabel(badge_3_frame, textvariable=achievement_unlock_dates[3])

badge_3_frame.grid(row=1, column=0)
badge_3_name.grid(row=0, column=0)
badge_3_icon.grid(row=1, column=0)
badge_3_date.grid(row=2, column=0)

badge_4_frame = ctk.CTkFrame(root)
badge_4_name = ctk.CTkLabel(badge_4_frame, textvariable=achievement_names[4])
badge_4_icon = ctk.CTkLabel(badge_4_frame, text="", image=achievement_badges[4])
badge_4_date = ctk.CTkLabel(badge_4_frame, textvariable=achievement_unlock_dates[4])

badge_4_frame.grid(row=1, column=1)
badge_4_name.grid(row=0, column=0)
badge_4_icon.grid(row=1, column=0)
badge_4_date.grid(row=2, column=0)

root.mainloop()

