from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):

    createdOn = models.DateTimeField( auto_now_add = True )
    updatedOn = models.DateTimeField( auto_now = True )

    title = models.CharField( max_length = 255 )
    description = models.CharField( max_length = 255 )
    cover_photo = models.ImageField( upload_to="covers/", default = "covers/default.jpg", blank = True, null = True )
    content = models.TextField()
    category = models.CharField( max_length = 255, default = "uncategorized" )
    likes = models.ManyToManyField( User, related_name="post_likes")

    def likes_count( self ):
        return self.likes.count()

    def alreadyLiked( self, user ):
        if user.is_anonymous:
            return False
        return self.likes.filter( id=user.id ).exists()

    def comments_all( self ):
        return self.comments.all().order_by("createdOn")

    def comments_count( self ):
        return self.comments.count()

    def add_comment( self, user, content ):
        return Comment.objects.create(
            post=self,
            user=user,
            content=content
        )

class Comment(models.Model):

    createdOn = models.DateTimeField( auto_now_add = True )
    content = models.TextField()

    post = models.ForeignKey( Post, related_name="comments", on_delete=models.CASCADE )
    user = models.ForeignKey( User, related_name="comments", on_delete=models.CASCADE )