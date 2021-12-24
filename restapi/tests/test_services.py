from django.test import TestCase

from restapi.models import Player, LeagueUser, Game, PlayerGame
from restapi.services import PlayerService


class PlayerServiceTestCase(TestCase):
    def setUp(self) -> None:
        game_a = Game.objects.create(name='Game A', start_date='2021-10-11 00:00:00Z', end_date='2021-10-11 02:00:00Z')
        game_b = Game.objects.create(name='Game B', start_date='2021-10-11 09:00:00Z', end_date='2021-10-11 11:00:00Z')
        game_c = Game.objects.create(name='Game C', start_date='2021-10-11 12:00:00Z', end_date='2021-10-11 14:00:00Z')

        p1 = Player.objects.create(id=LeagueUser.objects.create_user('p1@domain.com', 'pass'), name='p1', height_cm=170)
        p2 = Player.objects.create(id=LeagueUser.objects.create_user('p2@domain.com', 'pass'), name='p2', height_cm=175)
        p3 = Player.objects.create(id=LeagueUser.objects.create_user('p3@domain.com', 'pass'), name='p3', height_cm=180)
        p4 = Player.objects.create(id=LeagueUser.objects.create_user('p4@domain.com', 'pass'), name='p4', height_cm=180)

        PlayerGame.objects.create(player=p1, game=game_a, score=10)
        PlayerGame.objects.create(player=p1, game=game_b, score=20)
        PlayerGame.objects.create(player=p1, game=game_c, score=30)

        PlayerGame.objects.create(player=p2, game=game_a, score=5)
        PlayerGame.objects.create(player=p2, game=game_b, score=15)
        PlayerGame.objects.create(player=p2, game=game_c, score=10)

        PlayerGame.objects.create(player=p3, game=game_a, score=15)
        PlayerGame.objects.create(player=p3, game=game_b, score=20)
        PlayerGame.objects.create(player=p3, game=game_c, score=10)

        PlayerGame.objects.create(player=p4, game=game_a, score=5)
        PlayerGame.objects.create(player=p4, game=game_b, score=10)
        PlayerGame.objects.create(player=p4, game=game_c, score=11)

    def test_filter_over_90_percentile(self):
        """Checks if players are filtered over the 90th percentile"""
        # totals {p1, p2, p3, p4} = 60, 30, 45, 26
        # 90th percentile in uniform distribution is min + (max - min) * 0.90 = 56
        # Should return all players with total score > 56 (p1)
        players = PlayerService.filter_players_over_percentile(90, Player.objects.all())

        self.assertTrue(players.exists())
        self.assertEqual(1, len(players))
        self.assertEqual('p1', players[0].name)

    def test_filter_over_50_percentile(self):
        """Checks if players are filtered over the 50th percentile"""
        # 50th percentile = 43
        # Should return all players with total score > 43 (p1, p3)
        players = PlayerService.filter_players_over_percentile(50, Player.objects.all())

        self.assertTrue(players.exists())
        self.assertEqual(2, len(players))
        self.assertEqual('p1', players[0].name)
        self.assertEqual('p3', players[1].name)
