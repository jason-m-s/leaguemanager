from rest_framework.permissions import BasePermission
from restapi.models import LeagueUser


class IsLeagueAdmin(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.user_type == LeagueUser.UserTypeChoice.ADMIN)


class IsLeagueCoach(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.user_type == LeagueUser.UserTypeChoice.COACH)


class IsLeaguePlayer(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.user_type == LeagueUser.UserTypeChoice.PLAYER)