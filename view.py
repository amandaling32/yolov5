from PIL import Image
import os
from os import listdir

src_images = "./images"

for img in os.listdir(src_images):
    width = image_path = os.path.join(src_images, img)

    image = Image.open(image_path)

    width = image.width
    height = image.height

color = (255, 255, 255)

view = Image.new('RGB', ((3 * width + 20), (2 * height + 10)), color)

i = 0

for img in os.listdir(src_images):
    image_path = os.path.join(src_images, img)

    image = Image.open(image_path)

    if i == 0:
        view.paste(image, (0, 0))
    elif i == 1:
        view.paste(image, (image.width+10, 0))
    elif i == 2:
        view.paste(image, (2 * image.width+20, 0))
    elif i == 3:
        view.paste(image, (0, image.height+10))
    elif i == 4:
        view.paste(image, (image.width+10, image.height+10))
    elif i == 5:
        view.paste(image, (2 * image.width+20, image.height+10))

    i = i+1

view.save(f"./image_view/{img}")

    