import os

from django.db import models
from django.contrib.auth.models import User

def avatar_upload_to( instance, filename ):
    base, ext = os.path.splitext( filename )
    username = instance.user.username
    return f"avatars/{username}{ext}"

class UserProfile( models.Model ):
    user = models.OneToOneField( User, on_delete = models.CASCADE )
    avatar = models.ImageField(
        upload_to=avatar_upload_to,
        blank=True,
        null=True,
        default="avatars/default.jpg"
    )