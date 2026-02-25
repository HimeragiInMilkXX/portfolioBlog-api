from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from django.middleware.csrf import get_token

from .models import UserProfile
from .serializers import (
    ProfileUpdateSerializer,
    RegisterSerializer,
    LoginSerializer,
    UserProfileSerializer,
    UserSerializer,
)

class RegisterView( APIView ):
    def post( self, request, *args, **kwargs ):
        serializer = RegisterSerializer( data = request.data )
        if serializer.is_valid( raise_exception=True ):
            user = serializer.save()
            profile, _ = UserProfile.objects.get_or_create( user = user )
            avatar = profile.avatar

            login( request, user )

            return Response( {

                "detail": "Registered",
                "user": {
                    "user_id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "avatar": avatar.name
                }

            }, status = status.HTTP_201_CREATED )
        return Response( serializer.errors, status = status.HTTP_400_BAD_REQUEST )

class LoginView( APIView ):
    def post( self, request, *args, **kwargs ):
        serializer = LoginSerializer( data = request.data )
        if not serializer.is_valid( raise_exception=True ):
            return Response( serializer.errors, status = status.HTTP_400_BAD_REQUEST )

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        try:
            user_obj = User.objects.get( email=email )
        except User.DoesNotExist:
            return Response(

                { "detail": "Invalid credentials" },
                status = status.HTTP_400_BAD_REQUEST

            )

        user = authenticate( request, username = user_obj.username, password = password )

        if user is None:
            return Response(

                { "detail": "Invalid credentials" },
                status = status.HTTP_400_BAD_REQUEST

            )

        profile, _ = UserProfile.objects.get_or_create( user = user )
        login( request, user )

        return Response(
            {"detail": "Logged in", "user": { "user_id": user.id, "username": user.username, "email": user.email, "avatar": profile.avatar.name }},
            status=status.HTTP_200_OK,
        )

class LogoutView( APIView ):
    def post( self, request, *args, **kwargs ):
        logout( request )
        return Response( { "detail": "Logged out" }, status=status.HTTP_200_OK )


class ProfileAvatarView( APIView ):
    permission_classes = [IsAuthenticated]
    parser_classes = ( MultiPartParser, FormParser )

    def post( self, request, *args, **kwargs ):
        profile, _ = UserProfile.objects.get_or_create( user = request.user )

        if profile.avatar and profile.avatar.name != "avatars/default.jpg":
            profile.avatar.delete(save=False)

        serializer = UserProfileSerializer( profile, data = request.data, partial = True )
        if serializer.is_valid( raise_exception=True ):
            serializer.save()
            avatar_url = (

                request.build_absolute_uri( profile.avatar.url )
                if profile.avatar
                else None

            )
            return Response( { "avatar": avatar_url }, status=status.HTTP_200_OK )
        return Response( serializer.errors, status=status.HTTP_400_BAD_REQUEST )

class MeView( APIView ):
    permission_classes = [IsAuthenticated]

    def get( self, request ):
        serializer = UserSerializer(request.user)
        profile, _ = UserProfile.objects.get_or_create( user = request.user )
        avatar = profile.avatar
        return Response( {
            "user": {
                "user_id": serializer.data["id"],
                "email": serializer.data["email"],
                "username": serializer.data["username"],
                "avatar": avatar.name
            }}, status=status.HTTP_200_OK )

class ProfileUpdateView( APIView ):
    permission_classes = [IsAuthenticated]

    def put( self, request ):
        user = request.user
        serializer = ProfileUpdateSerializer(

            instance = user,
            data = request.data,

        )
        serializer.is_valid( raise_exception = True )
        serializer.save()
        return Response({"detail": "Profile updated"}, status=status.HTTP_200_OK)

@ensure_csrf_cookie
def csrf(request):
    token = get_token(request)
    return JsonResponse( { "csrfToken": token })
