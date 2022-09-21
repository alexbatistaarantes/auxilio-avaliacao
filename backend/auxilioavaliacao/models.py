from django.db import models

def image_directory_path(instance, filename):
    return f"images/{filename}"

class Image(models.Model):
    file = models.ImageField(
        upload_to=image_directory_path,
        width_field='width',
        height_field='height',
        null=True, blank=True
    )
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)

class Region(models.Model):
    from_image = models.ForeignKey(Image, on_delete=models.CASCADE)
    file = models.ImageField(
        upload_to='regions',
        null=True, blank=True
    )
    label = models.CharField(max_length=50)
    x1 = models.IntegerField(null=True, blank=True)
    y1 = models.IntegerField(null=True, blank=True)
    x2 = models.IntegerField(null=True, blank=True)
    y2 = models.IntegerField(null=True, blank=True)
