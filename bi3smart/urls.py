from django.urls import path , include
from bi3smart.views import LoginViews,ClientViews,CategorieViews,ProduitViews,CommandeViews, LigneCommandeViews, RecommandationViews
from . import views

urlpatterns = [
   path('login',LoginViews.as_view()),
   path('Clients',ClientViews.as_view()),
   path('Categories',CategorieViews.as_view()),
   path('Produits',ProduitViews.as_view()),
   path('Commandes',CommandeViews.as_view()),
   path('Lignes_commande',LigneCommandeViews.as_view()),
   path('Recommandations',RecommandationViews.as_view()),
]
