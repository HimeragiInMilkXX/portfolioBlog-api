from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [ "id", "title", "description", "category", "cover_photo", "content", "createdOn", "updatedOn" ]
        extra_kwargs = { "cover_photo": { "required": False, "allow_null": True } }

class EmbeddedImgSerializer(serializers.Serializer):
    image = serializers.ImageField()

class CommentSerializer( serializers.ModelSerializer ):

    username = serializers.CharField( source="user.username", read_only=True )
    avatar = serializers.ImageField(
        source="user.userprofile.avatar", read_only=True
    )

    class Meta:
        model = Comment
        fields = [ "id", "content", "createdOn", "username", "avatar" ]