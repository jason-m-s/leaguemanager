from rest_framework.permissions import BasePermission
from restapi.models import LeagueUser, Player, Coach, Team


class IsLeagueAdmin(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.user_type == LeagueUser.UserTypeChoice.ADMIN)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsLeagueCoach(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.user_type == LeagueUser.UserTypeChoice.COACH)

    def has_object_permission(self, request, view, obj):
        if not self.has_permission(request, view):
            return False

        if isinstance(obj, Player):
            return obj.team_id is not None and obj.team_id == Coach.objects.get(pk=request.user.id).team_id

        if isinstance(obj, Team):
            return obj.id == Coach.objects.get(pk=request.user.id).team_id

        return False


class IsLeaguePlayer(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.user_type == LeagueUser.UserTypeChoice.PLAYER)

    def has_object_permission(self, request, view, obj):
        return False
