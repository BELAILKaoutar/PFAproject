# Generated by Django 3.2.5 on 2024-04-29 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bi3smart', '0006_rename_idadmin_produit_idprod'),
    ]

    operations = [
        migrations.AddField(
            model_name='produit',
            name='image',
            field=models.ImageField(null=True, upload_to='static/images/'),
        ),
    ]