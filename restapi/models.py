from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
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
    team = models.OneToOneField(Team, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "coach"


class Player(models.Model):
    username = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    height_cm = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)
    team = models.OneToOneField(Team, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "player"


class Game(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)
    players = models.ManyToManyField(Player)
    teams = models.ManyToManyField(Team, through='GameTeam')

    class Meta:
        db_table = "game"


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
