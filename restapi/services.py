from django.db.models import Sum, QuerySet
from django.db.models.functions import Coalesce

from restapi.facades import UserFacade


class PlayerService:

    @staticmethod
    def get_players(user) -> QuerySet:
        return UserFacade.get_all_players(user).order_by('created_date')

    @staticmethod
    def get_players_over_percentile(user, percentile) -> QuerySet:
        # TODO: Validate if 0 < percentile < 100
        player_scores = PlayerService.get_players(user) \
            .annotate(score=Coalesce(Sum('playergame__score'), 0))

        min_score = min(player_scores, key=lambda player_score: player_score.score).score
        max_score = max(player_scores, key=lambda player_score: player_score.score).score
        percentile_score = min_score + (max_score - min_score) * (percentile / 100)

        return player_scores.filter(score__gte=percentile_score).order_by('created_date')

    @staticmethod
    def get_player(user, player_id) -> QuerySet:
        return UserFacade.get_player(user, player_id)


class TeamService:

    @staticmethod
    def get_teams(user):
        return UserFacade.get_teams(user).order_by('name')
