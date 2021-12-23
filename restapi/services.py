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

        # A discrete uniform distribution is used (https://en.wikipedia.org/wiki/Discrete_uniform_distribution)
        # This was done to keep the calculation simple. An appropriate model needs to be investigated based on the
        # actual distribution of data for percentile filtering
        min_score = min(player_scores, key=lambda player_score: player_score.score).score
        max_score = max(player_scores, key=lambda player_score: player_score.score).score
        percentile_score = min_score + (max_score - min_score) * (percentile / 100)

        return player_scores.filter(score__gte=percentile_score).order_by('created_date')


class TeamService:

    @staticmethod
    def get_teams(user):
        return UserFacade.get_teams(user).order_by('name')
