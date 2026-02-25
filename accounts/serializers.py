from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile

class RegisterSerializer( serializers.Serializer ):
    email = serializers.EmailField()
    username = serializers.CharField( max_length=150 )
    password = serializers.CharField( min_length=6, max_length=20 )

    def validate_email( self, value ):
        if User.objects.filter( email = value ).exists():
            raise serializers.ValidationError( "Email already registered!" )
        return value

    def validate_username( self, value ):
        if User.objects.filter( username = value ).exists():
            raise serializers.ValidationError( "Username already taken" )
        return value

    def create( self, validated_data ):
        user = User.objects.create_user(
            username = validated_data["username"],
            email = validated_data["email"],
            password = validated_data["password"]
        )
        return user

class ProfileUpdateSerializer( serializers.Serializer ):

    email = serializers.EmailField()
    username = serializers.CharField( max_length=150 )

    def validate_email( self, value ):

        if User.objects.filter( email = value ).exclude(pk = self.instance.pk ).exists():
            raise serializers.ValidationError( "Email already registered!" )
        return value

    def validate_username( self, value ):
        if User.objects.filter( username = value ).exclude(pk = self.instance.pk ).exists():
            raise serializers.ValidationError( "Username already taken" )
        return value
    
    def update( self, instance, validated_data ):
        instance.email = validated_data.get("email", instance.email)
        instance.username = validated_data.get("username", instance.username)
        instance.save()
        return instance

class LoginSerializer( serializers.Serializer ):
    email = serializers.EmailField()
    password = serializers.CharField()

class UserProfileSerializer( serializers.ModelSerializer ):
    class Meta:
        model = UserProfile
        fields = ["avatar"]
        extra_kwargs = { "avatar": { "required": False } }

class UserSerializer( serializers.ModelSerializer ):
    class Meta:
        model = User
        fields = [ "id", "username", "email" ]
