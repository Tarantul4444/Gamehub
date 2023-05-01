from rest_framework import serializers
from .models import Game, Genre, User, Comment, Like


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class GameSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)

    class Meta:
        model = Game
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    game = GameSerializer()

    class Meta:
        model = Comment
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    game = GameSerializer()

    class Meta:
        model = Like
        fields = '__all__'
