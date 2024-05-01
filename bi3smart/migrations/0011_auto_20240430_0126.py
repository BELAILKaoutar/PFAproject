# Generated by Django 3.2.5 on 2024-04-30 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bi3smart', '0010_alter_produit_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produit',
            name='image',
        ),
        migrations.AddField(
            model_name='produit',
            name='image_url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
