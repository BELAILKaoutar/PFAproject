
import json
from pyexpat import model
from venv import logger
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
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
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from .forms import ProduitForm
#views pour le chatbot gemini pro
from django.http import JsonResponse
from django.views import View
import json


class LoginViews(APIView):
    permission_classes = [AllowAny] 
    def logout(request):
        return render(request, 'login.html')
    def index_view(request):
        return render(request, 'index.html')
    def services(request):
        return render(request, 'services.html')
    def blog(request):
        return render(request, 'blog.html')
    def index1(request):
        return render(request, 'chat.py')   
    def shop(request):
        produits = Produit.objects.all()  # Retrieve all Produit objects
        return render(request, 'shop.html', {'produits': produits}) 
    def aboutus(request):
        return render(request, 'about.html')   
    def indexAdmin_view(request):
        return render(request, 'indexAdmin.html')
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
                    return HttpResponseRedirect('/indexAdmin/')  # Redirect to '/index/' upon successful login
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
    def client(request):
        clients = Client.objects.all()  # Retrieve all Produit objects
        return render(request, 'client.html', {'clients': clients}) 
    def contact(request):
        return render(request, 'contact.html') 
    def add_client(request):
        if request.method == 'POST':
            nom = request.POST.get('nom')
            prenom = request.POST.get('prenom')
            adresse = request.POST.get('adresse')
            télé = request.POST.get('télé')
            message = request.POST.get('message')


            client = Client.objects.create(
                nom=nom,
                prenom=prenom,
                adresse=adresse,
                télé=télé,
                message=message
            )
            serializer = ClientSerializer(client)
            return Response({'message': 'Client created successfully', 'client': serializer.data}, status=201)               
        else:
            return render(request, '/contact/')
  
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
    def get(self, request):
        categories = Categorie.objects.all()
        serializer = CategorieSerializer(categories, many=True)
        return render(request, 'category.html', {'categories': serializer.data})
    def add_category(request):
        if request.method == 'POST':
            nom_cate = request.POST.get('nom_cate')
            categorie = Categorie.objects.create(nom_cate=nom_cate)
            serializer = CategorieSerializer(categorie)
            return redirect('/category/')  # Redirect to the category list page after adding
        else:
            return render(request, 'add_category.html')            

  
    def update(self, request):
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
    def update_category(request, code_cate):
        category = get_object_or_404(Categorie, code_cate=code_cate)

        if request.method == 'POST':
            # Retrieve the updated category name from the form data
            new_name = request.POST.get('nom_cate')
            
            # Update the category name
            category.nom_cate = new_name
            category.save()
            
            return redirect('/category/')
        else:
            return render(request, 'update_category.html', {'category': category})
    def delete_category(request, code_cate):
        category = get_object_or_404(Categorie, code_cate=code_cate)

        if request.method == 'POST':
            # If the user confirms deletion, delete the category
            if 'confirm_delete' in request.POST:
                category.delete()
                return redirect('/category/')
            # If the user cancels deletion, redirect back to the category list page
            elif 'cancel_delete' in request.POST:
                return redirect('/category/')
        else:
            # Render the confirmation template
            return render(request, 'delete_category.html', {'category': category})
#pour produit
class ProduitViews(APIView):
    permission_classes = [AllowAny] 
    def cart(request):
        produits = Produit.objects.all() 
        return render(request, 'cart.html', {'produits': produits})
    def  add(request):
        if request.method == 'POST':
            idProd=request.POST.get('idProd')
            nom=request.POST.get('nom')
            prix=request.POST.get('prix')
            qteTotal=request.POST.get('qteTotal')
            user = request.POST.get('user_id')
            categorie= request.POST.get('categorie_id')

            produit = Produit.objects.create(
                user=user,
                categorie=categorie,
            )
            serializer = ProduitSerializer(produit)
            return redirect('/produit/')  # Redirect to the category list page after adding
        else:
            # Fetch users and categories from the database
            users = User.objects.all()
            categories = Categorie.objects.all()
            
            print("Users:", users)  # Check if users are retrieved
            print("Categories:", categories)  # Check if categories are retrieved
            
            return render(request, 'add_produit.html', {'users': users, 'categories': categories})

 
    def add_produit(request):
        if request.method == 'POST':
            nom = request.POST.get('nom')
            prix = request.POST.get('prix')
            qteTotal = request.POST.get('qteTotal')
            user_id = request.POST.get('user_id')
            code_cate = request.POST.get('code_cate')
            image = request.FILES.get('image')

            # Get User and Categorie instances
            user = User.objects.get(pk=user_id)
            categorie = Categorie.objects.get(code_cate=code_cate)

            # Create Produit instance and save to the database
            produit = Produit.objects.create(
                nom=nom,
                prix=prix,
                qteTotal=qteTotal,
                user=user,
                categorie=categorie,
                image=image,
            )

            return redirect('/produit/')  # Redirect after successful form submission
        else:
            users = User.objects.all()
            categories = Categorie.objects.all()
            return render(request, 'add_produit.html', {'users': users, 'categories': categories})
    def update(self, request):
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
    """def delete_produit(self, request, idProd=None):
      idProd = request.query_params.get('idProd')
      try:
            produits = Produit.objects.get(idProd=idProd)
      except Produit.DoesNotExist:
                return Response({'error': 'Produit not found'}, status=404)
      produits.delete()
      return Response("Produit deleted succesfuly",status=200)"""
    def update_produit(request, idProd):
        produit = Produit.objects.get(pk=idProd)

        if request.method == 'POST':
            nom = request.POST.get('nom')
            prix = request.POST.get('prix')
            qteTotal = request.POST.get('qteTotal')
            user_id = request.POST.get('user_id')
            code_cate = request.POST.get('code_cate')
            image = request.FILES.get('image')

            print("Form data received:")
            print("Nom:", nom)
            print("Prix:", prix)
            print("QteTotal:", qteTotal)
            print("User ID:", user_id)
            print("Category Code:", code_cate)
            print("Image:", image)

            if image:
                print("Image file name:", image.name)

            # Get User and Categorie instances
            user = User.objects.get(pk=user_id)
            categorie = Categorie.objects.get(code_cate=code_cate)

            if image:
                print("Updating image...")

                # Save the image file to the media directory
                produit.nom = nom
                produit.prix = prix
                produit.qteTotal = qteTotal
                produit.user = user
                produit.categorie = categorie
                produit.image = image
                produit.save()

                print("Image updated successfully.")

                return redirect('/produit/')  # Redirect after successful form submission
            else:
                print("No image provided. Existing image will be retained.")

                # Update other fields without modifying the image
                produit.nom = nom
                produit.prix = prix
                produit.qteTotal = qteTotal
                produit.user = user
                produit.categorie = categorie
                produit.save()

        else:
            users = User.objects.all()
            categories = Categorie.objects.all()
            return render(request, 'update_produit.html', {'produit': produit, 'users': users, 'categories': categories})

    def delete_produit(request, idProd):
        produit = get_object_or_404(Produit, idProd=idProd)

        if request.method == 'POST':
            # If the user confirms deletion, delete the category
            if 'confirm_delete' in request.POST:
                produit.delete()
                return redirect('/produit/')
            # If the user cancels deletion, redirect back to the category list page
            elif 'cancel_delete' in request.POST:
                return redirect('/produit/')
        else:
            # Render the confirmation template
            return render(request, 'delete_produit.html', {'produit': produit})
    def search_products(request):
        query = request.GET.get('query')
        produits = Produit.objects.filter(nom__contains=query)
        serializer = ProduitSerializer(produits, many=True)
        return render(request, 'produit.html', {'produits': produits})
    def get(self, request):
        produits = Produit.objects.all()
        
        # Pagination
        paginator = Paginator(produits, 2)  # Show 2 produits per page
        page = request.GET.get('page', 1)
        try:
            produits_page = paginator.page(page)
        except PageNotAnInteger:
            produits_page = paginator.page(1)
        except EmptyPage:
            produits_page = paginator.page(paginator.num_pages)
        
        serializer = ProduitSerializer(produits_page, many=True)
        
        return render(request, 'produit.html', {'produits': produits_page, 'serializer_data': serializer.data})

    def list_produits(request):
        produits = Produit.objects.all()
        
        # Pagination
        paginator = Paginator(produits, 2)  # Show 2 produits per page
        page = request.GET.get('page', 1)
        try:
            produits_page = paginator.page(page)
        except PageNotAnInteger:
            produits_page = paginator.page(1)
        except EmptyPage:
            produits_page = paginator.page(paginator.num_pages)
        
        serializer = ProduitSerializer(produits_page, many=True)
        
        return render(request, 'produit.html', {'produits': produits_page, 'serializer_data': serializer.data})

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
    def cart(request):
        produits = Produit.objects.all() 
        return render(request, 'cart.html', {'produits': produits})
    def addpanier(request):
        if request.method == 'POST':
            nom = request.POST.get('nom')
            prix = request.POST.get('prix')
            qte_commandee = request.POST.get('qte_commandee')

            # Check if both nom, prix, and qte_commandee are not None
            if nom is not None and prix is not None and qte_commandee is not None:
                # Convert the prix to float and qte_commandee to int
                prix = float(prix)
                qte_commandee = int(qte_commandee)

                # Calculate the total
                total = prix * qte_commandee

                # Create a new LigneCommande instance
                LigneCommande.objects.create(
                    nom=nom,
                    prix=prix,
                    qte_commandee=qte_commandee,
                    total=total
                )

                # Return a success response
                return JsonResponse({'message': 'Product added to cart successfully'})
            else:
                # Handle the case where nom, prix, or qte_commandee are None
                return JsonResponse({'error': 'Invalid product information'})
        else:
            # If the request method is not POST, return an error response
            return JsonResponse({'error': 'Invalid request method'}, status=400)


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
    
#return render(request, 'index.html')
class ChatbotViews(View):
    def chat(request):
        return render(request, 'chatbot.py')
    def post(self, request):
        data = json.loads(request.body)
        question = data.get('question', '')

        if question:
            response = model.generate_content(question)
            return JsonResponse({"response": response.text})

        return JsonResponse({"response": "Aucune question fournie"}, status=400)