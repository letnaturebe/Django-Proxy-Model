from django.contrib.auth.models import User
from django.test import TestCase

from core.models import Game, Feed, Post


class GameTest(TestCase):
    def test_model(self):
        user = User.objects.create(username="a")
        user.save()
        game: Game = Game.objects.create(game_name="한게임", game_location="서울")
        self.assertEqual(game.game_name, "한게임")
        self.assertEqual(game.dtype, "game")
        self.assertEqual(game.dtype.label, "게임")

        post: Post = Post.objects.create(title="title", body="body")
        self.assertEqual(post.title, "title")
        self.assertEqual(post.body, "body")
        self.assertEqual(Feed.objects.count(), 2)
        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(Post.objects.count(), 1)

        # feed(game) add test
        game.add(user)
        self.assertEqual(game.joined_users.count(), 1)

        # feed(game) like test
        game.like()
        game.like()
        self.assertEqual(game.like_count, 2)
