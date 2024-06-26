from django.contrib.auth.models import AbstractUser
#from datetime import datetime, timezone
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    cin = models.CharField(max_length=20, blank=True, null=True)
    nom = models.CharField(max_length=150, blank=True, null=True)
    prenom = models.CharField(max_length=150, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    télé = models.CharField(max_length=10, blank=True, null=True)


class Categorie(models.Model):
    code_cate = models.AutoField(primary_key=True)
    nom_cate = models.CharField(max_length=150, blank=True, null=True)

class Produit(models.Model):
   idProd = models.AutoField(primary_key=True)
   nom = models.CharField(max_length=150, blank=True, null=True)
   prix = models.FloatField(blank=True, null=True)
   qteTotal = models.IntegerField(blank=True, null=True)

   user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
   categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
   image = models.ImageField(upload_to="media/images/", null=True, blank=True)


   #image = models.ImageField(upload_to='static/images/', null=True) 
   #image_url = models.CharField(max_length=200, blank=True, null=True)
   #image = models.CharField(max_length=200, blank=True, null=True)  
class Client(models.Model):
    idCli = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=150, blank=True, null=True)
    prenom = models.CharField(max_length=150, blank=True, null=True)
    adresse = models.CharField(max_length=150,blank=True,null=True)
    télé = models.CharField(max_length=10, blank=True, null=True)
    message = models.CharField(max_length=10, blank=True, null=True)

class Recommandation(models.Model):
    idRec = models.AutoField(primary_key=True) 
    message = models.CharField(max_length=150, blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

class Commande (models.Model):
    idCommande = models.AutoField(primary_key=True)
    dateCommande = models.DateTimeField(default=timezone.now, blank=True, null=True)
    ETAT_CHOICES= [
        ('A','Accepté'),
        ('R','Refusé'),
        ('EC ','En cours'),
    ]
    etatCommande = models.CharField(max_length=10, choices=ETAT_CHOICES, default='EC')
    client = models.ForeignKey(Client, on_delete=models.CASCADE)


class LigneCommande(models.Model):
    #produit = models.ForeignKey(Produit, on_delete=models.CASCADE,null=True)
    nom = models.CharField(max_length=150, blank=True, null=True)
    prix = models.FloatField(blank=True, null=True)
    qte_commandee = models.IntegerField(blank=True, null=True , default=1)
    total = models.FloatField(blank=True, null=True)

