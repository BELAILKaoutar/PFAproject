# Generated by Django 3.2.5 on 2024-04-19 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bi3smart', '0005_client_télé'),
    ]

    operations = [
        migrations.RenameField(
            model_name='produit',
            old_name='idAdmin',
            new_name='idProd',
        ),
    ]
