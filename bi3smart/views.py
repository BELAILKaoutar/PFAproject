
from django.shortcuts import render
from bi3smart.models import User,Produit, Client,Commande,Recommandation,LigneCommande,Categorie
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny, IsAuthenticated
from bi3smart.serializers import UserSerializer, CustomTokenObtainPairSerializer,ClientSerializer,ProduitSerializer,CategorieSerializer,CommandeSerializer,LigneCommandeSerializer,RecommandationSerializer
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import TokenObtainPairView
#from django.shortcuts import render


class LoginViews(APIView):
    permission_classes = [AllowAny] 
    def post(self, request):
            data = request.data.copy()
            email = data.get('email')
            password = data.get('password')
            cin = data.get('cin')
            nom = data.get('nom')
            prenom = data.get('prenom')
            age = data.get('age')
            username = data.get('username')
            adresse = data.get('adresse')
            télé = data.get('télé')

            if not email:
                return Response({'error': 'Email is required'}, status=400)
            if not password:
                return Response({'error': 'Password is required'}, status=400)
            # Validate other required fields as needed

            try:
                user = User.objects.get(email=email)
                return Response({'error': 'User with this email already exists.'}, status=400)
            except User.DoesNotExist:
                hashed_password = make_password(password)
                user = User.objects.create(
                    email=email,
                    password=hashed_password,
                    cin=cin,
                    nom=nom,
                    prenom=prenom,
                    age=age,
                    username=username,
                    adresse=adresse,
                    télé=télé
                )
                serializer = UserSerializer(user)
                return Response({'message': 'User created successfully', 'user': serializer.data}, status=201)

  
    def put(self, request):
        data = request.data.copy()
        email = data.get('email')
        user_id = data.get('user_id')

        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=404)

        # Check if the provided email is different from the current email of the user
        if email != user.email and User.objects.filter(email=email).exists():
            return Response({'error': 'User with this email already exists.'}, status=400)

        serializer = UserSerializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data

        return Response({'user': user_data}, status=200)

    def delete(self, request, user_id=None):
        user_id = request.query_params.get('user_id')
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
        user.delete()
        return Response("User deleted successfully", status=200)
