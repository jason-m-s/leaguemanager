from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Sum, Count


# Create your models here.
from django.db.models.functions import Coalesce


class Team(models.Model):
    name = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "team"


class Coach(models.Model):
    username = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "coach"


class Game(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)
    teams = models.ManyToManyField(Team, through='GameTeam')

    class Meta:
        db_table = "game"


class Player(models.Model):
    name = models.CharField(max_length=100)
    height_cm = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    games = models.ManyToManyField(Game, through='PlayerGame')

    class Meta:
        db_table = "player"

    def get_player_summary(self):
        summary = PlayerGame.objects.filter(player_id__exact=self.id) \
            .aggregate(total=Coalesce(Sum('score'), 0), count=Coalesce(Count('score'), 0))
        return [summary['total'], summary['count']]


class PlayerGame(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    class Meta:
        db_table = "player_game"


class GameEvent(models.Model):
    type = models.CharField(max_length=50)
    value = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)
    game = models.ForeignKey(Game, on_delete=models.RESTRICT)

    class Meta:
        db_table = "gameevent"


class GameTeam(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    score = models.IntegerField()

    class Meta:
        db_table = "game_team"
