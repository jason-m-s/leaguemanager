from django.http import HttpRequest
from django.test import TestCase
from rest_framework.request import Request

from restapi.models import Player, LeagueUser, Team, Coach
from restapi.permissions import IsLeagueAdmin, IsLeagueCoach, IsLeaguePlayer


class IsLeagueAdminTestCase(TestCase):
    def test_unauthenticated_user_fails_admin_permission(self):
        """Check if unauthenticated user fails to use admin permissions"""
        request = Request(HttpRequest())
        request.user = LeagueUser()

        self.assertFalse(IsLeagueAdmin().has_permission(request, None))
        self.assertFalse(IsLeagueAdmin().has_object_permission(request, None, None))

    def test_coach_fails_admin_permission(self):
        """Check if coach user fails to use admin permissions"""
        request = Request(HttpRequest())
        request.user = LeagueUser(user_type=LeagueUser.UserTypeChoice.COACH)

        self.assertFalse(IsLeagueAdmin().has_permission(request, None))
        self.assertFalse(IsLeagueAdmin().has_object_permission(request, None, None))

    def test_player_fails_admin_permission(self):
        """Checks if player user fails to use admin permissions"""
        request = Request(HttpRequest())
        request.user = LeagueUser(user_type=LeagueUser.UserTypeChoice.PLAYER)

        self.assertFalse(IsLeagueAdmin().has_permission(request, None))
        self.assertFalse(IsLeagueAdmin().has_object_permission(request, None, None))

    def test_admin_passes_admin_permission(self):
        """Checks if admin user successfully authorized to use admin permissions"""
        request = Request(HttpRequest())
        request.user = LeagueUser(user_type=LeagueUser.UserTypeChoice.ADMIN)

        self.assertTrue(IsLeagueAdmin().has_permission(request, None))
        self.assertTrue(IsLeagueAdmin().has_object_permission(request, None, None))


class IsLeagueCoachTestCase(TestCase):
    def setUp(self):
        team_a = Team.objects.create(name='Team A')
        team_b = Team.objects.create(name='Team B')

        p1_user = LeagueUser.objects.create(
            username='p1@domain.com', password='pass', user_type=LeagueUser.UserTypeChoice.PLAYER)
        Player.objects.create(id=p1_user, name='p1', height_cm=170, team=team_a)

        p2_user = LeagueUser.objects.create(
            username='p2@domain.com', password='pass', user_type=LeagueUser.UserTypeChoice.PLAYER)
        Player.objects.create(id=p2_user, name='p2', height_cm=175, team=team_b)

        c1_user = LeagueUser.objects.create(
            username='c1@domain.com', password='pass', user_type=LeagueUser.UserTypeChoice.COACH)
        Coach.objects.create(id=c1_user, team=team_a)

        no_team_coach_user = LeagueUser.objects.create(
            username='no_team_coach@domain.com', password='pass', user_type=LeagueUser.UserTypeChoice.COACH)
        Coach.objects.create(id=no_team_coach_user)

    def test_unauthenticated_user_fails_coach_permission(self):
        """Check if unauthenticated user fails coach permissions"""
        request = Request(HttpRequest())
        request.user = LeagueUser()

        self.assertFalse(IsLeagueCoach().has_permission(request, None))
        self.assertFalse(IsLeagueCoach().has_object_permission(request, None, None))

    def test_admin_fails_coach_permissions(self):
        """Check if admin user fails to use coach permissions"""
        request = Request(HttpRequest())
        request.user = LeagueUser(user_type=LeagueUser.UserTypeChoice.ADMIN)

        self.assertFalse(IsLeagueCoach().has_permission(request, None))
        self.assertFalse(IsLeagueCoach().has_object_permission(request, None, None))

    def test_admin_fails_player_permissions(self):
        """Check if player user fails to use coach permissions"""
        request = Request(HttpRequest())
        request.user = LeagueUser(user_type=LeagueUser.UserTypeChoice.PLAYER)

        self.assertFalse(IsLeagueCoach().has_permission(request, None))
        self.assertFalse(IsLeagueCoach().has_object_permission(request, None, None))

    def test_coach_passes_coach_permission(self):
        """Check if coach user successfully passes coach permissions"""
        request = Request(HttpRequest())
        request.user = LeagueUser.objects.get(username='c1@domain.com')

        self.assertTrue(IsLeagueCoach().has_permission(request, None))

    def test_no_team_coach_fails_coach_object_permission(self):
        """Checks if a coach with no team assigned fails object permissions"""
        request = Request(HttpRequest())
        request.user = LeagueUser.objects.get(username='no_team_coach@domain.com')
        player = Player.objects.get(id__username='p1@domain.com')
        team = Team.objects.get(pk=1)

        self.assertFalse(IsLeagueCoach().has_object_permission(request, None, player))
        self.assertFalse(IsLeagueCoach().has_object_permission(request, None, team))

    def test_unrelated_coach_fails_coach_object_permission(self):
        """Checks if a coach with an unrelated team assigned fails object permissions"""
        request = Request(HttpRequest())
        request.user = LeagueUser.objects.get(username='c1@domain.com')
        player = Player.objects.get(id__username='p2@domain.com')
        team = Team.objects.get(pk=2)

        self.assertFalse(IsLeagueCoach().has_object_permission(request, None, player))
        self.assertFalse(IsLeagueCoach().has_object_permission(request, None, team))

    def test_related_coach_passes_coach_object_permission(self):
        """Checks if a coach with no team assigned fails object permissions"""
        request = Request(HttpRequest())
        request.user = LeagueUser.objects.get(username='c1@domain.com')
        player = Player.objects.get(id__username='p1@domain.com')
        team = Team.objects.get(pk=1)

        self.assertTrue(IsLeagueCoach().has_object_permission(request, None, player))
        self.assertTrue(IsLeagueCoach().has_object_permission(request, None, team))


class IsLeaguePlayerTestCase(TestCase):
    def test_unauthenticated_user_fails_player_permission(self):
        """Checks if an unauthenticated user is denied player permission"""
        request = Request(HttpRequest())
        request.user = LeagueUser()

        self.assertFalse(IsLeaguePlayer().has_permission(request, None))
        self.assertFalse(IsLeaguePlayer().has_object_permission(request, None, None))

    def test_admin_user_fails_player_permission(self):
        """Checks if an admin user is denied player permission"""
        request = Request(HttpRequest())
        request.user = LeagueUser(user_type=LeagueUser.UserTypeChoice.ADMIN)

        self.assertFalse(IsLeaguePlayer().has_permission(request, None))
        self.assertFalse(IsLeaguePlayer().has_object_permission(request, None, None))

    def test_coach_user_fails_player_permission(self):
        """Checks if a coach user is denied player permission"""
        request = Request(HttpRequest())
        request.user = LeagueUser(user_type=LeagueUser.UserTypeChoice.COACH)

        self.assertFalse(IsLeaguePlayer().has_permission(request, None))
        self.assertFalse(IsLeaguePlayer().has_object_permission(request, None, None))

    def test_player_user_passes_player_permission_except_object(self):
        """Checks if a player user is succeeds player permission but is still denied object permission"""
        request = Request(HttpRequest())
        request.user = LeagueUser(user_type=LeagueUser.UserTypeChoice.PLAYER)

        self.assertTrue(IsLeaguePlayer().has_permission(request, None))
        self.assertFalse(IsLeaguePlayer().has_object_permission(request, None, None))
