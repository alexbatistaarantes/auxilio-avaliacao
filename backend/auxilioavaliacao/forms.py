from django.forms import ModelForm

from .models import Image, Region

class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ['file']

class RegionForm(ModelForm):
    class Meta:
        model = Region
        exclude = ('from_image','file')
