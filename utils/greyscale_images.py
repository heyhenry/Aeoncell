from PIL import Image, ImageOps

# convert image into a greyscale version
def greyscale_image(converting_image_filename, greyscaled_image_filename):
    img = Image.open(converting_image_filename)
    img = img.convert("LA")
    img.save(greyscaled_image_filename)

# filename = "img/achievements/first_drink_achievement.png"
# greyscaled_filename = "new_greyscaled_image.png"

img_filenames = [
    "img/achievements/locked_version/1_month_club.png",
    "img/achievements/locked_version/first_day.png",
    "img/achievements/locked_version/first_drink.png",
    "img/achievements/locked_version/first_sleep.png",
    "img/achievements/locked_version/first_steps.png",
    "img/achievements/locked_version/first_workout.png",
    "img/achievements/locked_version/heavy_lifter_I.png",
    "img/achievements/locked_version/heavy_lifter_II.png",
    "img/achievements/locked_version/hydrated_human_I.png",
    "img/achievements/locked_version/hydrated_human_II.png",
    "img/achievements/locked_version/new_profile.png",
    "img/achievements/locked_version/rep_warrior.png",
    "img/achievements/locked_version/set_it_off.png",
    "img/achievements/locked_version/sleep_maxxed.png",
    "img/achievements/locked_version/sleeping_beauty_I.png",
    "img/achievements/locked_version/sleeping_beauty_II.png",
    "img/achievements/locked_version/step_stacker_I.png",
    "img/achievements/locked_version/step_stacker_II.png",
    "img/achievements/locked_version/ten_exercises.png",
]

for filename in img_filenames:
    filepath_prefix_index = filename.rfind("/")
    filename_index = filename.rfind("g")
    greyscale_image(filename, f"img/achievements/unlocked_version/{filename[filepath_prefix_index+1:filename_index+1]}")

