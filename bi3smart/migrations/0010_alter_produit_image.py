# Generated by Django 3.2.5 on 2024-04-30 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bi3smart', '0009_alter_produit_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produit',
            name='image',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
