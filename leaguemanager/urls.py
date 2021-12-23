"""leaguemanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework_nested import routers

from restapi import views
from restapi.views import GameEventView

router = routers.DefaultRouter()
router.register(r'players', views.PlayerView, basename='players')
router.register(r'teams', views.TeamView, basename='teams')
router.register(r'games', views.GameView, basename='games')

games_router = routers.NestedSimpleRouter(router, r'games', lookup='games')
games_router.register(r'events', GameEventView, basename='game-events')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(games_router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]
