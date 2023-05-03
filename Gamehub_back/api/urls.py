from .views import *
from django.urls import path

urlpatterns = [
    # games
    path('', GamesView.as_view()),
    path('games/', GamesView.as_view()),
    path('games/<int:game_id>/', GameView.as_view()),
    path('recommend/<int:user_id>/', RecommendView.as_view()),
    # users
    path('users/', UsersView.as_view()),
    path('users/<int:user_id>/', UserView.as_view()),
    # comments
    path('games/<int:game_id>/comments/', CommentsView.as_view()),
    path('games/<int:game_id>/comments/<int:comment_id>/', CommentView.as_view()),
    # likes
    path('users/<int:user_id>/likes/', LikesView.as_view()),
    path('games/<int:game_id>/users/<int:user_id>/', LikeView.as_view()),
    # auth
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('refresh-token/', refresh_token, name='refresh-token'),
    path('logout/', logout, name='logout'),
]
