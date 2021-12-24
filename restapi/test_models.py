from django.test import TestCase

from restapi.models import Player, LeagueUser, Game, PlayerGame


class PlayerTestCase(TestCase):
    def setUp(self):
        game_a = Game.objects.create(name='Game A', start_date='2021-10-10 00:00:00Z', end_date='2021-10-10 02:00:00Z')
        game_b = Game.objects.create(name='Game B', start_date='2021-10-10 09:00:00Z', end_date='2021-10-10 11:00:00Z')
        game_c = Game.objects.create(name='Game C', start_date='2021-10-10 12:00:00Z', end_date='2021-10-10 14:00:00Z')

        p1_user = LeagueUser.objects.create_user('p1@domain.com', 'pass')
        player1 = Player.objects.create(id=p1_user, name='p1', height_cm=170)

        PlayerGame.objects.create(player=player1, game=game_a, score=20)
        PlayerGame.objects.create(player=player1, game=game_b, score=10)
        PlayerGame.objects.create(player=player1, game=game_c, score=15)

        benched_player_user = LeagueUser.objects.create_user('benched@domain.com', 'pass')
        Player.objects.create(id=benched_player_user, name='benched', height_cm=175)

    def test_benched_player_summary(self):
        player = Player.objects.get(id__username='benched@domain.com')
        total, count = player.get_player_summary()

        self.assertEqual(0, total)
        self.assertEqual(0, count)

    def test_active_player_summary(self):
        player = Player.objects.get(id__username='p1@domain.com')
        total, count = player.get_player_summary()

        self.assertEqual(45, total)
        self.assertEqual(3, count)