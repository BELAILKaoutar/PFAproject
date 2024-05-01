"""PFAproject URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static
from bi3smart.views import CategorieViews, LoginViews,ProduitViews,ClientViews


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',LoginViews.index_view, name='index_view'),
    path('indexAdmin/',LoginViews.indexAdmin_view, name='indexAdmin_view'),   
    path('login/',LoginViews.login_view, name='login_view'),
    path('signup/',LoginViews.signup, name='signup'),
        #category
    path('category/', CategorieViews.as_view(), name='get'),    
    path('category/add/', CategorieViews.add_category, name='add_category'),
    path('category/update/<str:code_cate>/', CategorieViews.update_category, name='update_category'),
    path('category/delete/<str:code_cate>/', CategorieViews.delete_category, name='delete_category'),
        #produit 
    path('produit/', ProduitViews.as_view(),name='get'),
    path('produit/add/', ProduitViews.add_produit, name='add_produit'),
    path('produit/update/<str:idProd>/', ProduitViews.update_produit, name='update_produit'),
    path('produit/delete/<str:idProd>/', ProduitViews.delete_produit, name='delete_produit'),
    path('chat/',LoginViews.index1, name='index1'),
    path('shop/',LoginViews.shop, name='shop'),
    path('aboutus/',LoginViews.aboutus, name='aboutus'), 
    path('cart/',LoginViews.cart, name='cart'), 
    path('services/',LoginViews.services, name='services'), 
    path('blog/',LoginViews.blog, name='blog'), 

    path('contact/',ClientViews.contact, name='contact'),
    path('contact/add/',ClientViews.add_client, name='add_client'),
    path('shop/add_to_cart/', ProduitViews.add_to_cart, name='add_to_cart'),

    #path('shop/',ProduitViews),
    path('api/',include('bi3smart.urls')),
    path('api-auth', include('rest_framework.urls')),
    path('api/token', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

