from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from restapi.facades import UserFacade
from restapi.models import Player, Team, Game, GameEvent
from restapi.permissions import IsLeagueAdmin, IsLeagueCoach
from restapi.serializers import PlayerSerializer, TeamSerializer, GameSerializer, GameEventSerializer
from restapi.services import PlayerService


class PlayerView(viewsets.ModelViewSet):
    """
    API endpoint that allows players to be viewed, and optionally filtered by percentile
    """
    model = Player
    serializer_class = PlayerSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & (IsLeagueAdmin | IsLeagueCoach)]

    def get_queryset(self):
        players = UserFacade.get_all_players(self.request.user)

        percentile = self.request.query_params.get('percentile')
        if percentile:
            players = PlayerService.filter_players_over_percentile(int(percentile), players)

        team_id = self.request.query_params.get('team_id')
        if team_id:
            players = players.filter(team_id__exact=team_id)

        return players.order_by('created_date')

    def get_object(self):
        obj = get_object_or_404(Player.objects.all(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj


class TeamView(viewsets.ModelViewSet):
    """
    API endpoint that allows teams to be viewed
    """
    model = Team
    serializer_class = TeamSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & (IsLeagueAdmin | IsLeagueCoach)]

    def get_queryset(self):
        return UserFacade.get_all_teams(self.request.user).order_by('name')

    def get_object(self):
        obj = get_object_or_404(Team.objects.all(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj


class GameView(viewsets.ModelViewSet):
    """
    API endpoint that allows games to be viewed
    """
    model = Game
    serializer_class = GameSerializer
    queryset = Game.objects.all().order_by('-end_date', '-created_date')
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class GameEventView(viewsets.ModelViewSet):
    """
    API endpoint that allows games events to be viewed
    """
    model = GameEvent
    serializer_class = GameEventSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GameEvent.objects\
            .filter(game_id__exact=self.kwargs['games_pk'])\
            .order_by('created_date')
