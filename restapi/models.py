from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Sum, Count
from django.db.models.functions import Coalesce


class LeagueUser(AbstractUser):
    class UserTypeChoice(models.TextChoices):
        ADMIN = 'ADM', 'Admin'
        COACH = 'CCH', 'Coach'
        PLAYER = 'PLY', 'Player'

    user_type = models.CharField(max_length=3, choices=UserTypeChoice.choices)


class Team(models.Model):
    name = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class Coach(models.Model):
    id = models.OneToOneField(LeagueUser, on_delete=models.CASCADE, primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)


class Game(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    teams = models.ManyToManyField(Team, through='GameTeam')


class Player(models.Model):
    id = models.OneToOneField(LeagueUser, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=150)
    height_cm = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    games = models.ManyToManyField(Game, through='PlayerGame')

    def get_player_summary(self):
        summary = PlayerGame.objects.filter(player_id__exact=self.id.id) \
            .aggregate(total=Coalesce(Sum('score'), 0), count=Coalesce(Count('score'), 0))
        return [summary['total'], summary['count']]


class PlayerGame(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    class Meta:
        unique_together = ('player_id', 'game_id')


class GameEvent(models.Model):
    type = models.CharField(max_length=50)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    game = models.ForeignKey(Game, on_delete=models.RESTRICT)


class GameTeam(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    score = models.IntegerField()

    class Meta:
        unique_together = ('game_id', 'team_id')
