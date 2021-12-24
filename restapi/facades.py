from django.db.models import QuerySet

from restapi.models import Player, Coach, Team, LeagueUser


class UserFacade:

    @staticmethod
    def get_all_players(user) -> QuerySet:
        players = Player.objects.none()

        if user.user_type == LeagueUser.UserTypeChoice.COACH:
            team_id = Coach.objects.get(pk=user.id).team_id
            if team_id is not None:
                players = Player.objects.filter(team_id__exact=team_id)

        if user.user_type == LeagueUser.UserTypeChoice.ADMIN:
            players = Player.objects.all()

        return players

    @staticmethod
    def get_all_teams(user) -> QuerySet:
        teams = Coach.objects.none()

        if user.user_type == LeagueUser.UserTypeChoice.COACH:
            team_id = Coach.objects.get(pk=user.id).team_id
            teams = Team.objects.filter(id__exact=team_id)

        if user.user_type == LeagueUser.UserTypeChoice.ADMIN:
            teams = Team.objects.all()

        return teams
