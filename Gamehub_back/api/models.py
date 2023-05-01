from django.db import models


class User(models.Model):
    name = models.CharField(max_length=30, default='Name')
    surname = models.CharField(max_length=50, default='Surname')
    email = models.CharField(max_length=30, default='user@gmail.com')
    password = models.CharField(max_length=30, default='user')
    image = models.TextField(max_length=256, default='https://cdn.pixabay.com/photo/2023/04/28/09/59/mower'
                                                     '-7956264_1280.jpg')

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Genre(models.Model):
    name = models.CharField(max_length=256, default='')

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'


class Game(models.Model):
    name = models.CharField(max_length=256, default='')
    description = models.TextField(default='')
    genres = models.ManyToManyField(Genre, related_name='genres')
    likes_count = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    release_date = models.DateTimeField()

    class Meta:
        verbose_name = 'Game'
        verbose_name_plural = 'Games'


class Comment(models.Model):
    author = models.ForeignKey(User, related_name='comment_author', on_delete=models.CASCADE)
    description = models.TextField(default='')
    game = models.ForeignKey(Game, related_name='comment_game', on_delete=models.CASCADE)
    date = models.DateTimeField()

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like_user')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='like_game')

    def save(self, *args, **kwargs):
        # обновляем количество лайков при создании или сохранении объекта Like
        self.game.likes_count = self.game.likes.count()
        self.game.save()
        super(Like, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # обновляем количество лайков при удалении объекта Like
        self.game.likes_count = self.game.likes.count()
        self.game.save()
        super(Like, self).delete(*args, **kwargs)
