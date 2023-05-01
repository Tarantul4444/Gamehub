from rest_framework.views import APIView, Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from .models import Game, Genre, User, Comment
from .serializer import UserSerializer, GameSerializer, GenreSerializer, CommentSerializer


class GamesView(APIView):
    def get(self, request):
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request):
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class GameView(APIView):
    def get_game(self, game_id):
        try:
            return Game.objects.get(id=game_id)
        except Game.DoesNotExist as e:
            return Response({'message': str(e)}, status=HTTP_404_NOT_FOUND)

    def get(self, request, game_id):
        game = self.get_game(game_id)
        serializer = GameSerializer(game)
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, game_id):
        game = self.get_game(game_id)
        serializer = GameSerializer(game)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, game_id):
        game = self.get_game(game_id)
        game.delete()
        return Response({'message': 'Deleted successfully'}, status=HTTP_200_OK)


class RecommendView(APIView):
    def get(self, request):
        games = Game.objects.prefetch_related('genres').all()
        genres_set = set()
        for game in games:
            for genre in game.genres.all():
                genres_set.add(genre)
        games = set()
        for genre in genres_set:
            games.add(Game.objects.all().filter(genres__name=genre.name))
        print(games)
        serializer = GameSerializer(*games, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
