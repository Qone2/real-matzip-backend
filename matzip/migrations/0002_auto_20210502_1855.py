# Generated by Django 3.2 on 2021-05-02 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matzip', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='matzip',
            name='url_320',
            field=models.CharField(default=None, max_length=4000),
        ),
        migrations.AlterField(
            model_name='matzip',
            name='url',
            field=models.CharField(max_length=4000),
        ),
    ]
