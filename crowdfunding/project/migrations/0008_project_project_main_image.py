# Generated by Django 4.1.1 on 2022-09-21 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0007_reviewrating'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='project_main_image',
            field=models.ImageField(null=True, upload_to='project/imgs'),
        ),
    ]
