from django.contrib import admin

from team.models import (
    Type,
    Team,
    Task,
)

admin.site.register(Type)
admin.site.register(Team)
admin.site.register(Task)
