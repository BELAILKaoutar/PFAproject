# Generated by Django 3.2.5 on 2024-04-30 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bi3smart', '0014_alter_produit_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='message',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
