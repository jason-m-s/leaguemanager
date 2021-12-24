from django.db.models import Sum, QuerySet
from django.db.models.functions import Coalesce


class PlayerService:

    @staticmethod
    def filter_players_over_percentile(percentile, player_qs) -> QuerySet:
        player_scores = player_qs.annotate(score=Coalesce(Sum('playergame__score'), 0))

        # A discrete uniform distribution is used (https://en.wikipedia.org/wiki/Discrete_uniform_distribution)
        # This was done to keep the calculation simple. An appropriate model needs to be investigated based on the
        # actual distribution of data for percentile filtering
        min_score = min(player_scores, key=lambda player_score: player_score.score).score
        max_score = max(player_scores, key=lambda player_score: player_score.score).score
        percentile_score = min_score + (max_score - min_score) * (percentile / 100)

        return player_scores.filter(score__gte=percentile_score)
