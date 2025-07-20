from PIL import Image, ImageDraw, ImageFilter

def create_rounded_background_achievement_icon(
    input_path,
    output_path,
    icon_size=(512, 512),
    bg_glow_color="#B19CD9",
    border_color="#9370DB", 
    inner_glow=True
):
    # Open and resize icon
    original = Image.open(input_path).convert("RGBA")
    icon = original.resize(icon_size,Image.Resampling.LANCZOS)
    
    # Create canvas with shadow
    canvas_size = (icon_size[0] + 40, icon_size[1] + 40)  # Extra space for effects
    canvas = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    
    # Create glow effect (behind icon)
    if inner_glow:
        glow = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(glow)
        draw.ellipse(
            [(20, 20), (icon_size[0] + 20, icon_size[1] + 20)],
            fill=bg_glow_color
        )
        glow = glow.filter(ImageFilter.GaussianBlur(15))
        canvas.alpha_composite(glow)
    
    # Create border (rounded square)
    border = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(border)
    draw.rounded_rectangle(
        [(10, 10), (icon_size[0] + 30, icon_size[1] + 30)],
        radius=15,
        fill=border_color,
        outline=None,
        width=0
    )
    canvas.alpha_composite(border)
    
    # Add icon (centered)
    canvas.alpha_composite(
        icon,
        dest=(
            (canvas_size[0] - icon_size[0]) // 2,
            (canvas_size[1] - icon_size[1]) // 2
        )
    )
    
    canvas.save(output_path)

# list of achievement filenames incl. filepath
img_filnames = [
    "img/achievements/1_month_club.png",
    "img/achievements/first_day_achievement.png",
    "img/achievements/first_drink_achievement.png",
    "img/achievements/first_sleep_achievement.png",
    "img/achievements/first_steps_achievement.png",
    "img/achievements/first_workout_achievement.png",
    "img/achievements/heavy_lifter_I.png",
    "img/achievements/heavy_lifter_II.png",
    "img/achievements/hydrated_human_I.png",
    "img/achievements/hydrated_human_II.png",
    "img/achievements/new_profile_achievement.png",
    "img/achievements/rep_warrior.png",
    "img/achievements/set_it_off.png",
    "img/achievements/sleep_maxxed.png",
    "img/achievements/sleeping_beauty_I.png",
    "img/achievements/sleeping_beauty_II.png",
    "img/achievements/step_stacker_I.png",
    "img/achievements/step_stacker_II.png",
    "img/achievements/ten_exercises_achievement.png",
]

# loop through and created altered 'steam' achievement style icons
for filename in img_filnames:
    filepath_prefix_index = filename.rfind("/")
    filename_index = filename.rfind("g")
    create_rounded_background_achievement_icon(
        input_path=filename,
        output_path=f"{filename[:filepath_prefix_index]}/altered/{filename[filepath_prefix_index+1:filename_index+1]}",
        bg_glow_color="#F5F0FF00",
        border_color="#9370DB",
        inner_glow=True
    )
