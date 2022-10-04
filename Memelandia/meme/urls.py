from django.urls import path
from meme.views import Forward, MemeDetailView, TagIndexView, addMemeView,MemeList, addCommentView, Like, DisLike

app_name='meme'

urlpatterns = [
    path("bacheca/<str:username>", MemeList.as_view(),name="bacheca"),
    path("creazione_meme", addMemeView.as_view(), name="add_meme"),
    path("tags/<slug:tag_slug>/", TagIndexView.as_view(), name="memes_by_tag"),
    path("meme_detail/<int:pk>", MemeDetailView.as_view(), name="meme_detail"),
    path("meme_detail/<int:pk>/add_comment", addCommentView.as_view(),name="add_comment"),
    path("meme_detail/<int:pk>/like", Like.as_view(),name="like"),
    path("meme_detail/<int:pk>/dislike", DisLike.as_view(),name="dislike"),
    path("meme_detail/<int:pk>/forward", Forward.as_view(), name="forward")
]  
