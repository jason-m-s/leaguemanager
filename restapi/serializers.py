from rest_framework import serializers

from restapi.models import Player, Team, Game, GameEvent, GameTeam


class PlayerSerializer(serializers.ModelSerializer):

    def to_representation(self, obj):
        data = super().to_representation(obj)

        if self.has_expand_summary():
            total, count = obj.get_player_summary()
            data['avg_score'] = (total / count) if count > 0 else 0
            data['game_count'] = count

        return data

    def has_expand_summary(self):
        expand_params = self.context['request'].GET.getlist('expand', [])
        return 'summary' in expand_params

    class Meta:
        model = Player
        fields = ['id', 'name', 'height_cm']


class TeamSerializer(serializers.ModelSerializer):

    def to_representation(self, obj):
        data = super().to_representation(obj)

        if self.has_expand_summary():
            total, count = obj.get_team_summary()
            data['avg_score'] = (total / count) if count > 0 else 0

        return data

    def has_expand_summary(self):
        expand_params = self.context['request'].GET.getlist('expand', [])
        return 'summary' in expand_params

    class Meta:
        model = Team
        fields = '__all__'


class GameTeamForGameSerializer(serializers.ModelSerializer):
    team_id = serializers.SerializerMethodField()
    team_name = serializers.SerializerMethodField()

    @staticmethod
    def get_team_id(obj):
        return obj.team.id

    @staticmethod
    def get_team_name(obj):
        return obj.team.name

    class Meta:
        model = GameTeam
        fields = ['id', 'team_id', 'team_name', 'score']


class GameSerializer(serializers.ModelSerializer):
    teams = GameTeamForGameSerializer(source='gameteam_set', many=True)

    class Meta:
        model = Game
        depth = 1
        fields = ['id', 'name', 'start_date', 'end_date', 'created_date', 'updated_date', 'teams']


class GameEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = GameEvent
        fields = ['type', 'description', 'created_date', 'updated_date']
