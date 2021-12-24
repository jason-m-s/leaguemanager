from django.test import TestCase

from restapi.facades import UserFacade
from restapi.models import Player, LeagueUser, Coach, Team


class UserFacadeTestCase(TestCase):
    def setUp(self):
        team_a = Team.objects.create(name='Team A')
        team_b = Team.objects.create(name='Team B')

        p1_user = LeagueUser.objects.create(
            username='p1@domain.com', password='pass', user_type=LeagueUser.UserTypeChoice.PLAYER)
        player1 = Player.objects.create(id=p1_user, name='p1', height_cm=170, team=team_a)

        p2_user = LeagueUser.objects.create(
            username='p2@domain.com', password='pass', user_type=LeagueUser.UserTypeChoice.PLAYER)
        player2 = Player.objects.create(id=p2_user, name='p2', height_cm=175, team=team_b)

        c1_user = LeagueUser.objects.create(
            username='c1@domain.com', password='pass', user_type=LeagueUser.UserTypeChoice.COACH)
        coach1 = Coach.objects.create(id=c1_user, team=team_a)

        admin_user = LeagueUser.objects.create(
            username='admin@domain.com', password='pass', user_type=LeagueUser.UserTypeChoice.ADMIN)

        no_team_coach_user = LeagueUser.objects.create(
            username='no_team_coach@domain.com', password='pass', user_type=LeagueUser.UserTypeChoice.COACH)
        no_team_coach = Coach.objects.create(id=no_team_coach_user)

    # Player loading test cases
    def test_players_for_unauthenticated_user(self):
        """Checks if an unauthenticated user returns an empty player list"""
        players = UserFacade.get_all_players(LeagueUser())
        self.assertFalse(players.exists())

    def test_players_for_coach_without_team(self):
        """Checks if a coach with no team assigned returns an empty player list"""
        coach = LeagueUser.objects.get(username='no_team_coach@domain.com')
        players = UserFacade.get_all_players(coach)
        self.assertFalse(players.exists())

    def test_players_for_coach_with_team(self):
        """Checks if coach with a team set returns players in that list only"""
        coach = LeagueUser.objects.get(username='c1@domain.com')
        players = UserFacade.get_all_players(coach)

        self.assertTrue(players.exists())
        self.assertEqual(1, len(players))
        self.assertEqual('p1', players[0].name)

    def test_players_for_admin_user(self):
        """Checks if admin user will return all players as list"""
        admin = LeagueUser.objects.get(username='admin@domain.com')
        players = UserFacade.get_all_players(admin)

        self.assertTrue(players.exists())
        self.assertEqual(2, len(players))

    # Team loading test cases
    def test_teams_for_unauthenticated_user(self):
        """Checks if unauthenticated user returns and empty team list"""
        teams = UserFacade.get_all_teams(LeagueUser())
        self.assertFalse(teams.exists())

    def test_teams_for_coach_without_team(self):
        """Checks if coach without team returns an empty team list"""
        coach = LeagueUser.objects.get(username='no_team_coach@domain.com')
        teams = UserFacade.get_all_teams(coach)
        self.assertFalse(teams.exists())

    def test_teams_for_coach_with_team(self):
        """Checks if coach with team returns only assigned team in list"""
        coach = LeagueUser.objects.get(username='c1@domain.com')
        teams = UserFacade.get_all_teams(coach)

        self.assertTrue(teams.exists())
        self.assertEqual(1, len(teams))
        self.assertEqual('Team A', teams[0].name)

    def test_teams_for_admin_user(self):
        """Checks if admin user returns all teams as list"""
        admin = LeagueUser.objects.get(username='admin@domain.com')
        teams = UserFacade.get_all_players(admin)

        self.assertTrue(teams.exists())
        self.assertEqual(2, len(teams))
