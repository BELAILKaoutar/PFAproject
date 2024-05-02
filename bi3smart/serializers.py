from rest_framework import serializers
from bi3smart.models import User,Produit, Client,Commande,Recommandation,LigneCommande,Categorie
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email

        return token
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
class CommandeSerializer(serializers.ModelSerializer):
    
    def required(value):
        if value is None:
            raise serializers.ValidationError('This command is required')
    class Meta:
        model = Commande
        fields = '__all__'
    

class ProduitSerializer(serializers.ModelSerializer):
    categorie = serializers.CharField(source='categorie.nom_cate', read_only=True)
    user = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Produit
        fields = '__all__'
class LigneCommandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LigneCommande
        fields = '__all__'

class RecommandationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommandation
        fields = '__all__'

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = '__all__'