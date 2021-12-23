from rest_framework import serializers

from restapi.models import Player, PlayerGame, Team, Game, GameEvent


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
    class Meta:
        model = Team
        fields = '__all__'


class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = ['name', 'start_date', 'end_date', 'created_date', 'updated_date']


class GameEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = GameEvent
        fields = ['type', 'description', 'created_date', 'updated_date']