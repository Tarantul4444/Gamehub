from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView, Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from .models import Game, Genre, User, Comment, Like
from .serializer import UserSerializer, GameSerializer, GenreSerializer, CommentSerializer, LikeSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import datetime
import jwt


SECRET_KEY = 'django-insecure-yo!pe^3-a70y)z!b$36^l(qlnwno6x35ub8jx)8oo@&e17n2ya'


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
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        likes = Like.objects.filter(user=user)
        games = set()
        for like in likes:
            games.add(like.game)
        genres_set = set()
        for game in games:
            genres = game.genres.all()
            for genre in genres:
                genres_set.add(genre)
        games = set()
        for genre in genres_set:
            for game in Game.objects.all().filter(genres__name=genre.name):
                games.add(game.id)
        games = Game.objects.filter(id__in=list(games))
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class UsersView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserView(APIView):
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist as e:
            return Response({'message': str(e)}, status=HTTP_404_NOT_FOUND)

    def get(self, request, user_id):
        user = self.get_user(user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, user_id):
        user = self.get_user(user_id)
        serializer = UserSerializer(user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        user = self.get_user(user_id)
        user.delete()
        return Response({'message': 'Deleted successfully'}, status=HTTP_200_OK)


class CommentsView(APIView):
    def get(self, request, game_id):
        comments = Comment.objects.all().filter(game__id=game_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request, game_id):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class CommentView(APIView):
    def get_comment(self, game_id, comment_id):
        try:
            return Comment.objects.get(id=comment_id, game__id=game_id)
        except Comment.DoesNotExist as e:
            return Response({'message': str(e)}, status=HTTP_404_NOT_FOUND)

    def get(self, request, game_id, comment_id):
        comment = self.get_comment(game_id, comment_id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, game_id, comment_id):
        comment = self.get_comment(game_id, comment_id)
        serializer = CommentSerializer(comment)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, game_id, comment_id):
        comment = self.get_comment(game_id, comment_id)
        comment.delete()
        return Response({'message': 'Deleted successfully'}, status=HTTP_200_OK)


class LikesView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        try:
            like = Like.objects.all().filter(user=user)
        except Like.DoesNotExist as e:
            return Response({'message': 'Like error'}, status=HTTP_400_BAD_REQUEST)
        serializer = LikeSerializer(like, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class LikeView(APIView):
    def get(self, request, game_id, user_id):
        game = get_object_or_404(Game, id=game_id)
        user = get_object_or_404(User, id=user_id)
        try:
            like = Like.objects.get(game=game, user=user)
        except Like.DoesNotExist as e:
            return Response({'message': 'Like error'}, status=HTTP_400_BAD_REQUEST)
        serializer = LikeSerializer(like)
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, game_id, user_id):
        game = get_object_or_404(Game, id=game_id)
        user = get_object_or_404(User, id=user_id)
        try:
            like = Like.objects.get(game=game, user=user)
            like.delete()
        except Like.DoesNotExist as e:
            like = Like.objects.create(game=game, user=user)
            like.save()

        serializer = LikeSerializer(like)
        return Response(serializer.data, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = User.objects.filter(email=email, password=password)[0]
    if not user:
        return Response({'error': 'Invalid Credentials'}, status=400)

    # Generate Access Token
    access_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat': datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(access_token_payload, SECRET_KEY)

    # Generate Refresh Token
    refresh_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),
        'iat': datetime.datetime.utcnow(),
    }
    refresh_token = jwt.encode(refresh_token_payload, SECRET_KEY)

    return Response({'access_token': access_token, 'refresh_token': refresh_token}, status=200)


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    refresh_token = request.data.get('refresh_token')
    if not refresh_token:
        return Response({'error': 'Refresh Token is required'}, status=400)

    try:
        refresh_token_payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=['HS256'])
        user = User.objects.get(id=refresh_token_payload['user_id'])
    except jwt.ExpiredSignatureError:
        return Response({'error': 'Refresh Token Expired'}, status=400)
    except (jwt.InvalidTokenError, User.DoesNotExist):
        return Response({'error': 'Invalid Refresh Token'}, status=400)

    # Generate new Access Token
    access_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat': datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(access_token_payload, SECRET_KEY).decode('utf-8')

    return Response({'access_token': access_token}, status=200)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    name = request.data.get('name')
    surname = request.data.get('surname')
    email = request.data.get('email')
    password = request.data.get('password')
    image = request.data.get('image')
    if not name or not surname or not email or not password:
        return Response({'error': 'All fields are required'}, status=400)
    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already exists'}, status=400)
    user = User.objects.create(name=name, surname=surname, email=email, password=password, image=image)

    # Generate Access Token
    access_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat': datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(access_token_payload, SECRET_KEY).decode('utf-8')

    # Generate Refresh Token
    refresh_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),
        'iat': datetime.datetime.utcnow(),
    }
    refresh_token = jwt.encode(refresh_token_payload, SECRET_KEY).decode('utf-8')

    return Response({'access_token': access_token, 'refresh_token': refresh_token}, status=201)


@api_view(['POST'])
def logout(request):
    response = Response({'success': 'Successfully logged out'}, status=200)
    response.delete_cookie('access_token')
    return response


