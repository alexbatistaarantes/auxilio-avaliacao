from PIL import Image

def crop_image(image, box):
    image = Image.open(image)
    image.crop(box).show()
    #return image.crop(box)
