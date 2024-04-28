
from venv import logger
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from grpc import Status
from requests import request
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
from rest_framework import status
from rest_framework.renderers import JSONRenderer

class LoginViews(APIView):
    permission_classes = [AllowAny] 
    def index_view(request):
        return render(request, 'index.html')
    def signup(request):
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            cin = request.POST.get('cin')
            nom = request.POST.get('nom')
            prenom = request.POST.get('prenom')
            age = request.POST.get('age')
            username = request.POST.get('username')
            adresse = request.POST.get('adresse')
            télé = request.POST.get('télé')

            if not email:
                return HttpResponse({'error': 'Email is required'}, status=400)
            if not password:
                return HttpResponse({'error': 'Password is required'}, status=400)
            # Validate other required fields as needed

            try:
                user = User.objects.get(email=email)
                return HttpResponse({'error': 'User with this email already exists.'}, status=400)
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
                return HttpResponse({'message': 'User created successfully', 'user': serializer.data}, status=201)
                
        else:
             return render(request, 'signup.html')

    def login_view(request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = None

            if user is not None:
                if check_password(password, user.password):
                    request.session['user_id'] = user.user_id
                    return HttpResponseRedirect('/index/')  # Redirect to '/index/' upon successful login
                else:
                    return HttpResponse("Invalid login credentials. Please try again.")
            else:
                return HttpResponse("Invalid login credentials. Please try again.")

        return render(request, 'login.html')

  
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
    


#pour Client

class ClientViews(APIView):
    permission_classes = [AllowAny] 
    def post(self, request):
            data = request.data.copy()
            nom = data.get('nom')
            prenom = data.get('prenom')
            adresse = data.get('adresse')
            télé = data.get('télé')


            client = Client.objects.create(
                nom=nom,
                prenom=prenom,
                adresse=adresse,
                télé=télé
            )
            serializer = ClientSerializer(client)
            return Response({'message': 'Client created successfully', 'client': serializer.data}, status=201)               

  
    def put(self, request):
        data = request.data.copy()
        idCli = data.get('idCli')

        try:
            client = Client.objects.get(idCli=idCli)
        except Client.DoesNotExist:
            return Response({'error': 'Client not found.'}, status=404)

        # Check if the provided email is different from the current email of the user
        #if email != user.email and User.objects.filter(email=email).exists():
        #    return Response({'error': 'User with this email already exists.'}, status=400)

        serializer = ClientSerializer(client, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        client_data = serializer.data

        return Response({'client': client_data}, status=200)

    def delete(self, request, idCli=None):
        idCli = request.query_params.get('idCli')
        try:
            client = Client.objects.get(idCli=idCli)
        except Client.DoesNotExist:
            return Response({'error': 'Client not found'}, status=404)
        client.delete()
        return Response("Client deleted successfully", status=200)

# pour catégorie

class CategorieViews(APIView):
    permission_classes = [AllowAny] 
    def post(self, request):
            data = request.data.copy()
            code_cate = data.get('code_cate')
            nom_cate = data.get('nom_cate')



            categorie = Categorie.objects.create(
                code_cate=code_cate,
                nom_cate=nom_cate,
            )
            serializer = CategorieSerializer(categorie)
            return Response({'message': 'Categorie created successfully', 'categorie': serializer.data}, status=201)               

  
    def put(self, request):
        data = request.data.copy()
        code_cate = data.get('code_cate')

        try:
            categorie = Categorie.objects.get(code_cate=code_cate)
        except Categorie.DoesNotExist:
            return Response({'error': 'Categorie not found.'}, status=404)

        serializer = CategorieSerializer(categorie, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        categorie_data = serializer.data

        return Response({'categorie': categorie_data}, status=200)

    def delete(self, request, code_cate=None):
        code_cate = request.query_params.get('code_cate')
        try:
            categorie = Categorie.objects.get(code_cate=code_cate)
        except Categorie.DoesNotExist:
            return Response({'error': 'Categorie not found'}, status=404)
        categorie.delete()
        return Response("Categorie deleted successfully", status=200)
    
#pour produit
class ProduitViews(APIView):
    def post(self, request):
        required_keys = ['nom', 'prix', 'qteTotal', 'code_cate']
        if not all(key in request.data for key in required_keys):
            return Response({'error': 'All product fields are required'}, 400)

        produit = Produit.objects.create(
            nom=request.data.get('nom'),
            prix=request.data.get('prix'),
            qteTotal=request.data.get('qteTotal'),
            user_id=request.data.get('user_id'),  # Assuming you have authenticated users
            categorie_id=request.data.get('code_cate'),  # Assuming 'code_cate' refers to the categorie_id
        )
        produit.save()

        return Response({'message': 'Product created successfully'})

class ProduitViews(APIView):
    permission_classes = [AllowAny] 
    def post(self, request):
        data = request.data.copy()
        idProd=request.data.get('idProd')
        nom=request.data.get('nom')
        prix=request.data.get('prix')
        qteTotal=request.data.get('qteTotal')
        user_id = data.get('user_id')
        categorie_id= data.get('categorie_id')



        produit = Produit.objects.create(
            user_id=user_id,
            categorie_id=categorie_id,
        )
        serializer = ProduitSerializer(produit)
        return Response({'message': 'Produit created successfully', 'produit': produit.data}, status=201)        


    def put(self, request):
        idProd=request.data.get('idProd')
        nom=request.data.get('nom')
        prix=request.data.get('prix')
        qteTotal=request.data.get('qteTotal')
        user_id = request.data.get('user_id')
        code_cate = request.data.get('code_cate')
        produit = Produit.objects.create(
            nom = request.data.get('nom'),
            prix = request.data.get('prix'),
            qteTotal= request.data.get('qteTotal'),
            user_id =user_id,
            code_cate =code_cate,
        )
        produit.save()
        return Response({
            'message': 'Produit created successfully',
        })
    def delete(self, request, idProd=None):
      idProd = request.query_params.get('idProd')
      try:
            produits = Produit.objects.get(idProd=idProd)
      except Produit.DoesNotExist:
                return Response({'error': 'Produit not found'}, status=404)
      produits.delete()
      return Response("Produit deleted succesfuly",status=200)
    
class CommandeViews(APIView):
    permission_classes = [AllowAny] 
    def post(self, request):
        data = request.data.copy()
        idCommande=request.data.get('idCommande')
        dateCommande=request.data.get('dateCommande')
        etatCommande=request.data.get('etatCommande')
        client_id=request.data.get('client_id')
        commande = Commande.objects.create(
            client_id=client_id,
        )
        serializer = CommandeSerializer(commande)
        return Response({'message': 'Command created successfully', 'commande': commande.data}, status=201) 
    def delete(self, request, idCommande=None):
        idCommande= request.query_params.get('idCommande')
        try:
            commandes = Commande.objects.get(idCommande=idCommande)
        except Commande.DoesNotExist:
                return Response({'error': 'Commande not found'}, status=404)
        commandes.delete()
        return Response("Commande deleted succesfuly",status=200) 
class LigneCommandeViews(APIView):
    permission_classes = [AllowAny] 
    def post(self, request):
        data = request.data.copy()
        qte_commandee=request.data.get('qte_commandee')
        commande_id=request.data.get('commande_id')
        produit_id=request.data.get('produit_id')

        ligneCommande = LigneCommande.objects.create(
            commande_id=commande_id,
            produit_id=produit_id,
        )
        serializer = LigneCommandeSerializer(ligneCommande)
        return Response({'message': 'Line Command created successfully', 'ligneCommande': ligneCommande.data}, status=201) 

class RecommandationViews(APIView):
    permission_classes = [AllowAny] 
    def post(self, request):
        data = request.data.copy()
        idRec=request.data.get('idRec')
        message=request.data.get('message')
        client_id=request.data.get('client_id')

        recommandation = Recommandation.objects.create(
            client_id=client_id,
        )
        serializer = RecommandationSerializer(recommandation)
        return Response({'message': 'Recommandation created successfully', 'recommandation': recommandation.data}, status=201)
    def delete(self, request, idRec=None):
        idRec = request.query_params.get('idRec')
        try:
            recommandations = Recommandation.objects.get(idRec=idRec)
        except Recommandation.DoesNotExist:
                return Response({'error': 'Recommandation not found'}, status=404)
        recommandations.delete()
        return Response("Recommandation deleted succesfuly",status=200) 