from rest_framework import viewsets

from restapi.models import Player, Team, Game, GameEvent
from restapi.serializers import PlayerSerializer, TeamSerializer, GameSerializer, GameEventSerializer
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


class GameView(viewsets.ModelViewSet):
    """
    API endpoint that allows games to be viewed
    """
    model = Game
    serializer_class = GameSerializer
    queryset = Game.objects.all().order_by('-end_date', '-created_date')


class GameEventView(viewsets.ModelViewSet):
    """
    API endpoint that allows games events to be viewed
    """
    model = GameEvent
    serializer_class = GameEventSerializer

    def get_queryset(self):
        return GameEvent.objects.filter(game_id__exact=self.kwargs['games_pk'])