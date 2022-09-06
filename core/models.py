from typing import Optional

from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _


class FeedType(models.TextChoices):
    POST = 'post', _('포스트')
    GAME = 'game', _('게임')
    TEAM = 'team', _('팀')


class Feed(models.Model):
    class FeedManager(models.Manager):
        def get_queryset(self):
            queryset: QuerySet = super().get_queryset()
            dtype: Optional[str] = getattr(self, 'TYPE', None)
            if dtype is not None:
                queryset = queryset.filter(dtype=dtype)
            return queryset

        def create(self, **kwargs):
            return super().create(**kwargs, dtype=self.TYPE)

    title = models.CharField(max_length=128)
    body = models.TextField()
    dtype = models.CharField(
        max_length=10,
        choices=FeedType.choices,
        default=FeedType.POST,
    )
    like_count = models.PositiveIntegerField(default=0)
    joined_users = models.ManyToManyField(User, blank=True)
    game_name = models.CharField(max_length=128)
    game_location = models.CharField(max_length=128)
    room_name = models.CharField(max_length=128)

    objects = FeedManager()

    def add(self, user: User):
        self.joined_users.add(user)

    def like(self):
        self.like_count += 1
        self.save()


class Post(Feed):
    class PostManager(Feed.FeedManager):
        TYPE = FeedType.POST

    objects = PostManager()

    class Meta:
        proxy = True

    def __str__(self):
        return f'{self.title}'


class Game(Feed):
    class GameManager(Feed.FeedManager):
        TYPE = FeedType.GAME

    objects = GameManager()

    class Meta:
        proxy = True

    def __str__(self):
        return f'{self.game_name}'
