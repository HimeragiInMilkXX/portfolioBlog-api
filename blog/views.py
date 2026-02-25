from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from blog.models import Comment, Post
from django.db.models import Q

from .serializers import CommentSerializer, PostSerializer
from .serializers import EmbeddedImgSerializer
from django.shortcuts import get_object_or_404
import uuid, os

class PostView(APIView):
    parser_classes = ( MultiPartParser, FormParser )

    def post(self, request, *args, **kwargs):
        serializer = PostSerializer( data = request.data )
        if serializer.is_valid():
            post = serializer.save()
            return Response( PostSerializer(post).data, status = status.HTTP_201_CREATED )
        return Response( serializer.errors, status = status.HTTP_400_BAD_REQUEST )

    def get( self, request, id, *args, **kwargs ):
        post = get_object_or_404( Post, pk = id )
        serializer = PostSerializer(post)
        return Response(serializer.data, status = status.HTTP_200_OK )

class GetPostView( APIView ):

    def get( self, request, *args, **kwargs ):
        keyword = request.query_params.get( "keyword", "" )
        posts = Post.objects.filter(
            Q( title__icontains=keyword ) | Q( description__icontains=keyword ) | Q( category__icontains=keyword )
        ).order_by( "-createdOn" )
        serializer = PostSerializer( posts, many = True )
        return Response( serializer.data, status=status.HTTP_200_OK )

class EmbedImgUploadView(APIView):
    parser_classes = ( MultiPartParser, )

    def post (self, request, *args, **kwargs):
        print( request.data )
        serializer = EmbeddedImgSerializer( data = request.data )
        if serializer.is_valid():
            image = serializer.validated_data["image"]

            from django.core.files.storage import default_storage
            from django.core.files.base import ContentFile

            _, ext = os.path.splitext( image.name )

            path = default_storage.save(
                f"embedded/{str(uuid.uuid4())}{ext}", ContentFile(image.read())
            )

            url = request.build_absolute_uri( settings.MEDIA_URL + path )
            return Response( { "url": url }, status = status.HTTP_201_CREATED )
        
        return Response( serializer.errors, status = status.HTTP_400_BAD_REQUEST )
    
class LikeView( APIView ):

    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [ perm() for perm in permission_classes ]

    def get( self, request, id, *args, **kwargs ):
        post = Post.objects.get( id=id )
        return Response( {
            "likes": post.likes_count(),
            "alreadyLiked": post.alreadyLiked(request.user)
        }, status=status.HTTP_200_OK )

    def post( self, request, id, *args, **kwargs ):
        post = Post.objects.get( id=id )
        user = request.user

        if post.likes.filter( id = user.id ).exists():
            post.likes.remove( user )
            liked = False
        else:
            post.likes.add( user )
            liked = True

        return Response( { "liked": liked, "likes": post.likes_count() }, status=status.HTTP_200_OK )

class CommentView( APIView ):

    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [ perm() for perm in permission_classes ]

    def get( self, request, id, *args, **kwargs ):
        post = Post.objects.get( id=id )
        serializer = CommentSerializer( post.comments_all(), many = True )
        return Response( {
            "comments_count": post.comments_count(),
            "comments": serializer.data
        }, status=status.HTTP_200_OK )

    def post( self, request, id, *args, **kwargs ):
        post = get_object_or_404( Post, id=id )
        user = request.user
        content = request.data["content"]
        print( request.data['content'] )
        Comment.objects.create(
            post=post,
            user=user,
            content=content
        )
        return Response( { "detail": "Comment added" }, status=status.HTTP_200_OK )