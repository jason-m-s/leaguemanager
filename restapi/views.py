from rest_framework import viewsets

from restapi.models import Player, Team
from restapi.serializers import PlayerSerializer, TeamSerializer
from restapi.services import PlayerService, TeamService


class PlayerView(viewsets.ModelViewSet):
    """
    API endpoint that allows players to be viewed, and optionally filtered by percentile
    """
    model = Player
    serializer_class = PlayerSerializer

    def get_queryset(self):
        user = self.request.user
        percentile = self.request.query_params.get('percentile')

        if percentile:
            return PlayerService.get_players_over_percentile(user, int(percentile))
        else:
            return PlayerService.get_players(self.request.user)


class TeamView(viewsets.ModelViewSet):
    """
    API endpoint that allows teams to be viewed
    """
    model = Team
    serializer_class = TeamSerializer

    def get_queryset(self):
        return TeamService.get_teams(self.request.user)

