from django.contrib.auth import get_user_model
from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS,
)

from team.models import Team


class IsTeamMemberOrIsAdmin(BasePermission):
    def has_permission(self, request, view):
        team_id = view.kwargs.get("pk")

        if request.method in SAFE_METHODS:
            if team_id:
                is_team_member = get_user_model().objects.filter(
                        id=request.user.id, team__id=team_id
                )
                if is_team_member:
                    return True
        else:
            if team_id and request.user.is_leader:
                return True

        return request.user.is_staff


class IsUsersTaskOrIsAdmin(BasePermission):
    def has_permission(self, request, view):
        task_id = view.kwargs.get("pk")

        if request.method in SAFE_METHODS:
            if task_id:
                is_team_member = get_user_model().objects.filter(
                    id=request.user.id, team__isnull=False
                )

                if not is_team_member:
                    return request.user.is_staff

                is_team_have_tasks = Team.objects.filter(
                    id=is_team_member[0].team.id, tasks__isnull=False
                )

                if (
                    is_team_have_tasks
                    and is_team_have_tasks[0].tasks.filter(
                        id=task_id
                    ).exists()
                ):
                    return True
        else:
            if task_id and request.user.is_leader:
                return True

        return request.user.is_staff
