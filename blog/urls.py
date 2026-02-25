from django.urls import path
from .views import CommentView, GetPostView, LikeView, PostView, EmbedImgUploadView

urlpatterns = [
    path("posts/create", PostView.as_view(), name="post-create" ),
    path("posts/get", GetPostView.as_view(), name="post-fetch"),
    path("posts/<int:id>", PostView.as_view(), name="post-get-by-id"),
    path("posts/<int:id>/like", LikeView.as_view(), name="post-like" ),
    path("posts/<int:id>/comment", CommentView.as_view(), name="post-comment"),
    path("image/embed", EmbedImgUploadView.as_view(), name="embed-image-upload" ),
]