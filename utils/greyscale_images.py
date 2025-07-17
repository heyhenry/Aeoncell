from PIL import Image, ImageOps

# convert image into a greyscale version
def greyscale_image(converting_image_filename, greyscaled_image_filename):
    img = Image.open(converting_image_filename)
    img = img.convert("LA")
    img.save(greyscaled_image_filename)

filename = "img/achievements/first_drink_achievement.png"
greyscaled_filename = "new_greyscaled_image.png"

greyscale_image(filename, greyscaled_filename)
