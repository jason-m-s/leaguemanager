from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from restapi.models import LeagueUser

# Register your models here.
admin.site.register(LeagueUser, UserAdmin)
