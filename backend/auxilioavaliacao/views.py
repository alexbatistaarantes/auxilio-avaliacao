from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.files.base import ContentFile

from .models import Image, Region
from .forms import ImageForm, RegionForm
import base64

def home(request):
    """ Homepage com a lista de todas as imagens criadas
    """

    images = Image.objects.all()
    context = { 'images': images }
    return render(request, 'auxilioavaliacao/home.html', context)

def new_image(request):
    """ Formulário para inserir nova imagem
        - Se inserção bem sucedida, redireciona para a página da imagem inserida
    """

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()
            return HttpResponseRedirect(reverse('auxilioavaliacao:image', args=[image.id]))
    else:
        form = ImageForm()

    context = {'form': form}
    return render(request, 'auxilioavaliacao/new_image.html', context)

def image(request, image_id):
    """ Mostra a imagem e suas regiões
    """

    image = get_object_or_404(Image, pk=image_id)
    return render(request, 'auxilioavaliacao/image.html', {'image': image})

def new_region(request, image_id):
    """ Ferramenta de seleção de uma nova região de uma imagem
        - Se bem sucedido, redireciona para a página da imagem
    """
    
    image = get_object_or_404(Image, pk=image_id)
    if request.method == "POST":
        form = RegionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            region = Region(**data, from_image=image)
            region.save()

            # Salva a imagem da região a partir do campo da imagem em base64, feita pelo Croppie
            format, file_base64 = request.POST['image_base64'].split(';base64,')
            extension = format.split('/')[-1]
            file = ContentFile(base64.b64decode(file_base64))
            filename = f"{region.id}.{extension}"
            region.file.save(filename, file, save=True)

            return HttpResponseRedirect(reverse('auxilioavaliacao:image', args=[image.id]))
    else:
        form = RegionForm()

    context = {
        'image': image,
        'form': form
    }
    return render(request, 'auxilioavaliacao/new_region.html', context)

def region(request, image_id, region_id):
    """ Página da região
    """

    image = get_object_or_404(Image, pk=image_id)
    region = get_object_or_404(Region, pk=region_id)
    context = {
        'image': image,
        'region': region
    }
    return render(request, 'auxilioavaliacao/region.html', context)
