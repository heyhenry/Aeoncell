from PIL import Image, ImageDraw, ImageFilter

def create_rounded_background_achievement_icon(
    input_path,
    output_path,
    icon_size=(512, 512),
    bg_glow_color="#B19CD9",
    border_color="#9370DB",
    inner_glow=True,
    icon_scale=0.8,
    corner_radius=30,
    border_width=3, 
    outer_border_color="#E0E0E0" 
):
    # open and resize icon
    original = Image.open(input_path).convert("RGBA")
    scaled_icon_size = (int(icon_size[0] * icon_scale), (int(icon_size[1] * icon_scale)))
    icon = original.resize(scaled_icon_size, Image.Resampling.LANCZOS)
    
    # create canvas with shadow
    canvas_size = (icon_size[0] + 40, icon_size[1] + 40)
    canvas = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    
    # create rounded background mask
    background_mask = Image.new("L", canvas_size, 0)
    draw = ImageDraw.Draw(background_mask)
    draw.rounded_rectangle(
        [(0, 0), canvas_size],
        radius=corner_radius,
        fill=255
    )
    
    # create outer border (neutral color)
    outer_border = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(outer_border)
    draw.rounded_rectangle(
        [(0, 0), canvas_size],
        radius=corner_radius,
        outline=outer_border_color,
        width=border_width
    )
    canvas.alpha_composite(outer_border)
    
    # create glow effect with rounded corners
    if inner_glow:
        glow = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(glow)
        draw.rounded_rectangle(
            [(border_width+5, border_width+5), (canvas_size[0]-(border_width+5), canvas_size[1]-(border_width+5))],
            radius=corner_radius-5,
            fill=bg_glow_color
        )
        glow = glow.filter(ImageFilter.GaussianBlur(15))
        canvas.alpha_composite(glow)
    
    # create main border
    border = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(border)
    draw.rounded_rectangle(
        [(border_width+5, border_width+5), (canvas_size[0]-(border_width+5), canvas_size[1]-(border_width+5))],
        radius=corner_radius-5,
        fill=border_color,
        outline=None,
        width=0
    )
    canvas.alpha_composite(border)
    
    # add icon (centered)
    canvas.alpha_composite(
        icon,
        dest=(
            (canvas_size[0] - scaled_icon_size[0]) // 2,
            (canvas_size[1] - scaled_icon_size[1]) // 2
        )
    )
    
    # apply rounded corners to final composition
    rounded_canvas = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    rounded_canvas.paste(canvas, (0, 0), background_mask)
    
    rounded_canvas.save(output_path)

# list of achievement filenames incl. filepath
img_filenames = [
    "img/achievements/original_icons/1_month_club.png",
    "img/achievements/original_icons/first_day.png",
    "img/achievements/original_icons/first_drink.png",
    "img/achievements/original_icons/first_sleep.png",
    "img/achievements/original_icons/first_steps.png",
    "img/achievements/original_icons/first_workout.png",
    "img/achievements/original_icons/heavy_lifter_I.png",
    "img/achievements/original_icons/heavy_lifter_II.png",
    "img/achievements/original_icons/hydrated_human_I.png",
    "img/achievements/original_icons/hydrated_human_II.png",
    "img/achievements/original_icons/new_profile.png",
    "img/achievements/original_icons/rep_warrior.png",
    "img/achievements/original_icons/set_it_off.png",
    "img/achievements/original_icons/sleep_maxxed.png",
    "img/achievements/original_icons/sleeping_beauty_I.png",
    "img/achievements/original_icons/sleeping_beauty_II.png",
    "img/achievements/original_icons/step_stacker_I.png",
    "img/achievements/original_icons/step_stacker_II.png",
    "img/achievements/original_icons/ten_exercises.png",
]

for filename in img_filenames:
    filepath_prefix_index = filename.rfind("/")
    filename_index = filename.rfind("g")
    create_rounded_background_achievement_icon(
        input_path=filename,
        output_path=f"img/achievements/unlocked_version/{filename[filepath_prefix_index+1:filename_index+1]}",
        bg_glow_color="#F5F0FF00",
        border_color="#9370DB",
        inner_glow=True,
        icon_scale=0.8,
        corner_radius=30
    )