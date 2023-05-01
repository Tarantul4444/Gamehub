from django.contrib import admin
from .models import Game, Genre, User, Comment


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'genres', 'likes_count', 'price', 'release_date')
    search_fields = ('name', 'genres')
    list_filter = ('name',)

    def genres(self):
        return self.genres.count()


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'email', 'password', 'image')
    search_fields = ('name', 'email')
    list_filter = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'description', 'game', 'date')
    search_fields = ('game', 'date')
    list_filter = ('game',)