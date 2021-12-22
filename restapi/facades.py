from django.db.models import QuerySet

from restapi.models import Player, Coach, Team


class UserFacade:

    @staticmethod
    def get_all_players(user) -> QuerySet:
        if user == 'COACH':
            # TODO: Get PK from user
            # TODO: Validate if coach has team set
            coach = Coach.objects.get(pk=1)
            return Player.objects.filter(team_id__exact=coach.id)

        return Player.objects.all()

    @staticmethod
    def get_player(user, player_id) -> QuerySet:
        if user == 'COACH':
            # TODO: Get PK from user
            # TODO: Validate if coach has team set
            # TODO: Validate if coach has permissions to this team
            coach = Coach.objects.get(pk=1)

        return Player.objects.get(pk=player_id)

    @staticmethod
    def get_teams(user) -> QuerySet:
        if user == 'COACH':
            # TODO: Get PK from user
            coach = Coach.objects.get(pk=1)
            return Team.objects.none() if coach.team_id is None else Team.objects.filter(team_id__exact=coach.team_id)

        return Team.objects.all()
