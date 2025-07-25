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
print(achievement_names)
results = [(6, 'new_profile', 'Unlocked 25 Jul, 2025, 09:07 AM'), (1, 'first_day', 'Unlocked 25 Jul, 2025, 08:44 AM'), (2, 'first_drink', ''), (3, 'first_sleep', '')]
for i in range(len(results)):
    if results[i][2] == "":
        continue
    achievement_names[i+1] = results[i][1]
    achievement_badges[i+1] = f"achievement: {results[i][0]} badge here"
    achievement_unlock_dates[i+1] = results[i][2]

for i in range(1, 5):
    print(f"==========[Badge Slot {i}]==========")
    print(f"Achievement Name: {achievement_names[i]}")
    print(f"Achievement Badge: {achievement_badges[i]}")
    print(f"Achievement Unlock Date: {achievement_unlock_dates[i]}")
    print("=====================================\n")

