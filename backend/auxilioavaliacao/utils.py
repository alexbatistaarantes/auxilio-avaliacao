from PIL import Image
from os.path import splitext
from io import BytesIO
from django.core.files import File

def crop_image(image, box):
    img = Image.open(image)
    # Obtendo a extensão
    extension = splitext(image.name)[-1][1:]
    # Corta a imagem
    cropped = img.crop(box)
    # Salvando em um BytesIO
    cropped_IO = BytesIO()
    cropped.save(cropped_IO, format=extension)
    # Salvando em um File do Django
    cropped_file = File(cropped_IO, name=image.name)
    
    return cropped_file
