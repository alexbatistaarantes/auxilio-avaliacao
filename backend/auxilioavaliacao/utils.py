from email.mime import base
from PIL import Image
from os.path import basename, splitext
from io import BytesIO
from django.core.files import File

def crop_image(image, box):
    img = Image.open(image)
    # Obtendo a extensão
    _, extension = split_filename_and_extension(image.name)
    # Corta a imagem
    cropped = img.crop(box)
    # Salvando em um BytesIO
    cropped_IO = BytesIO()
    cropped.save(cropped_IO, format=extension)
    # Salvando em um File do Django
    cropped_file = File(cropped_IO, name=image.name)
    
    return cropped_file

def split_filename_and_extension(filepath):
    splitted = splitext(basename(filepath))
    return splitted[0], splitted[-1][1:]
