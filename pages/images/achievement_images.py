import customtkinter as ctk
from PIL import Image

achievements_triple_stars = ctk.CTkImage(light_image=Image.open("img/achievements/original_icons/triple_stars.png"), dark_image=Image.open("img/achievements/original_icons/triple_stars.png"), size=(128, 96))
achievements_banner = ctk.CTkImage(light_image=Image.open("img/achievements/original_icons/achievement_banner.png"), dark_image=Image.open("img/achievements/original_icons/achievement_banner.png"), size=(96, 96))
loading_achievement_icon = ctk.CTkImage(light_image=Image.open("img/achievements/original_icons/loading_achievement.png"), dark_image=Image.open("img/achievements/original_icons/loading_achievement.png"), size=(96, 96))

locked_achievements = {
   1 : ctk.CTkImage(light_image=Image.open("img/achievements/locked_version/first_day.png"), dark_image=Image.open("img/achievements/locked_version/first_day.png"), size=(96, 96)),
   2 : ctk.CTkImage(light_image=Image.open("img/achievements/locked_version/first_day.png"), dark_image=Image.open("img/achievements/locked_version/first_day.png"), size=(96, 96)),
   3 : ctk.CTkImage(light_image=Image.open("img/achievements/locked_version/first_day.png"), dark_image=Image.open("img/achievements/locked_version/first_day.png"), size=(96, 96)),
   4 : ctk.CTkImage(light_image=Image.open("img/achievements/locked_version/first_day.png"), dark_image=Image.open("img/achievements/locked_version/first_day.png"), size=(96, 96)),
   5 : ctk.CTkImage(light_image=Image.open("img/achievements/locked_version/first_day.png"), dark_image=Image.open("img/achievements/locked_version/first_day.png"), size=(96, 96)),
   6 : ctk.CTkImage(light_image=Image.open("img/achievements/locked_version/first_day.png"), dark_image=Image.open("img/achievements/locked_version/first_day.png"), size=(96, 96)),
   7 : ctk.CTkImage(light_image=Image.open("img/achievements/locked_version/first_day.png"), dark_image=Image.open("img/achievements/locked_version/first_day.png"), size=(96, 96)),
   8 : ctk.CTkImage(light_image=Image.open("img/achievements/locked_version/first_day.png"), dark_image=Image.open("img/achievements/locked_version/first_day.png"), size=(96, 96)),
   9 : ctk.CTkImage(light_image=Image.open("img/achievements/locked_version/first_day.png"), dark_image=Image.open("img/achievements/locked_version/first_day.png"), size=(96, 96)),
   10 : ctk.CTkImage(light_image=Image.open("img/achievements/locked_version/first_day.png"), dark_image=Image.open("img/achievements/locked_version/first_day.png"), size=(96, 96)),
   11 : ctk.CTkImage(light_image=Image.open("img/achievements/locked_version/first_day.png"), dark_image=Image.open("img/achievements/locked_version/first_day.png"), size=(96, 96)),
   12 : ctk.CTkImage(light_image=Image.open("img/achievements/locked_version/first_day.png"), dark_image=Image.open("img/achievements/locked_version/first_day.png"), size=(96, 96)),
   13 : ctk.CTkImage(light_image=Image.open("img/achievements/locked_version/first_day.png"), dark_image=Image.open("img/achievements/locked_version/first_day.png"), size=(96, 96)),
   14 : ctk.CTkImage(light_image=Image.open("img/achievements/locked_version/first_day.png"), dark_image=Image.open("img/achievements/locked_version/first_day.png"), size=(96, 96)),
   15 : ctk.CTkImage(light_image=Image.open("img/achievements/locked_version/first_day.png"), dark_image=Image.open("img/achievements/locked_version/first_day.png"), size=(96, 96)),
   16 : ctk.CTkImage(light_image=Image.open("img/achievements/locked_version/first_day.png"), dark_image=Image.open("img/achievements/locked_version/first_day.png"), size=(96, 96)),
   17 : ctk.CTkImage(light_image=Image.open("img/achievements/locked_version/first_day.png"), dark_image=Image.open("img/achievements/locked_version/first_day.png"), size=(96, 96)),
   18 : ctk.CTkImage(light_image=Image.open("img/achievements/locked_version/first_day.png"), dark_image=Image.open("img/achievements/locked_version/first_day.png"), size=(96, 96)),
   19 : ctk.CTkImage(light_image=Image.open("img/achievements/locked_version/first_day.png"), dark_image=Image.open("img/achievements/locked_version/first_day.png"), size=(96, 96))
}

unlocked_achievements = {
   1 : ctk.CTkImage(light_image=Image.open("img/achievements/unlocked_version/first_day.png"), dark_image=Image.open("img/achievements/unlocked_version/first_day.png"), size=(96, 96)),
   2 : ctk.CTkImage(light_image=Image.open("img/achievements/unlocked_version/first_day.png"), dark_image=Image.open("img/achievements/unlocked_version/first_day.png"), size=(96, 96)),
   3 : ctk.CTkImage(light_image=Image.open("img/achievements/unlocked_version/first_day.png"), dark_image=Image.open("img/achievements/unlocked_version/first_day.png"), size=(96, 96)),
   4 : ctk.CTkImage(light_image=Image.open("img/achievements/unlocked_version/first_day.png"), dark_image=Image.open("img/achievements/unlocked_version/first_day.png"), size=(96, 96)),
   5 : ctk.CTkImage(light_image=Image.open("img/achievements/unlocked_version/first_day.png"), dark_image=Image.open("img/achievements/unlocked_version/first_day.png"), size=(96, 96)),
   6 : ctk.CTkImage(light_image=Image.open("img/achievements/unlocked_version/first_day.png"), dark_image=Image.open("img/achievements/unlocked_version/first_day.png"), size=(96, 96)),
   7 : ctk.CTkImage(light_image=Image.open("img/achievements/unlocked_version/first_day.png"), dark_image=Image.open("img/achievements/unlocked_version/first_day.png"), size=(96, 96)),
   8 : ctk.CTkImage(light_image=Image.open("img/achievements/unlocked_version/first_day.png"), dark_image=Image.open("img/achievements/unlocked_version/first_day.png"), size=(96, 96)),
   9 : ctk.CTkImage(light_image=Image.open("img/achievements/unlocked_version/first_day.png"), dark_image=Image.open("img/achievements/unlocked_version/first_day.png"), size=(96, 96)),
   10 : ctk.CTkImage(light_image=Image.open("img/achievements/unlocked_version/first_day.png"), dark_image=Image.open("img/achievements/unlocked_version/first_day.png"), size=(96, 96)),
   11 : ctk.CTkImage(light_image=Image.open("img/achievements/unlocked_version/first_day.png"), dark_image=Image.open("img/achievements/unlocked_version/first_day.png"), size=(96, 96)),
   12 : ctk.CTkImage(light_image=Image.open("img/achievements/unlocked_version/first_day.png"), dark_image=Image.open("img/achievements/unlocked_version/first_day.png"), size=(96, 96)),
   13 : ctk.CTkImage(light_image=Image.open("img/achievements/unlocked_version/first_day.png"), dark_image=Image.open("img/achievements/unlocked_version/first_day.png"), size=(96, 96)),
   14 : ctk.CTkImage(light_image=Image.open("img/achievements/unlocked_version/first_day.png"), dark_image=Image.open("img/achievements/unlocked_version/first_day.png"), size=(96, 96)),
   15 : ctk.CTkImage(light_image=Image.open("img/achievements/unlocked_version/first_day.png"), dark_image=Image.open("img/achievements/unlocked_version/first_day.png"), size=(96, 96)),
   16 : ctk.CTkImage(light_image=Image.open("img/achievements/unlocked_version/first_day.png"), dark_image=Image.open("img/achievements/unlocked_version/first_day.png"), size=(96, 96)),
   17 : ctk.CTkImage(light_image=Image.open("img/achievements/unlocked_version/first_day.png"), dark_image=Image.open("img/achievements/unlocked_version/first_day.png"), size=(96, 96)),
   18 : ctk.CTkImage(light_image=Image.open("img/achievements/unlocked_version/first_day.png"), dark_image=Image.open("img/achievements/unlocked_version/first_day.png"), size=(96, 96)),
   19 : ctk.CTkImage(light_image=Image.open("img/achievements/unlocked_version/first_day.png"), dark_image=Image.open("img/achievements/unlocked_version/first_day.png"), size=(96, 96))
}