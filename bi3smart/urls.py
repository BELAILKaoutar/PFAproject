from django.urls import path , include
from bi3smart.views import LoginViews
from . import views

urlpatterns = [
   path('login',LoginViews.as_view()),


]
""", ClientViews,CommandeViews,ProduitViews, LigneCommandeViews, RecommandationViews, CategorieViews"""
"""path('Clients',ClientViews.as_view()),
   path('Commandes',CommandeViews.as_view()),
   path('Produits',ProduitViews.as_view()),
   path('Lignes_commande',LigneCommandeViews.as_view()),
   path('Recommandations',RecommandationViews.as_view()),
   path('Categories',CategorieViews.as_view()),"""