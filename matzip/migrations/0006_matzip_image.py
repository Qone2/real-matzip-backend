# Generated by Django 3.2 on 2021-05-21 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matzip', '0005_remove_matzip_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='matzip',
            name='image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
