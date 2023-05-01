from .views import *
from django.urls import path


urlpatterns = [
    path('', GamesView.as_view()),
    path('games/', GamesView.as_view()),
    path('games/<int:game_id>/', GameView.as_view()),
    path('recommend/', RecommendView.as_view()),
]