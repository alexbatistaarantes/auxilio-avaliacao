# Generated by Django 4.1.1 on 2022-09-21 17:16

import auxilioavaliacao.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auxilioavaliacao', '0010_alter_image_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='file',
            field=models.ImageField(blank=True, height_field='height', null=True, upload_to=auxilioavaliacao.models.image_directory_path, width_field='width'),
        ),
    ]
