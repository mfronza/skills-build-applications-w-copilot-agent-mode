from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Activity, Leaderboard, Team, UserProfile, Workout
from .serializers import (
    ActivitySerializer,
    LeaderboardSerializer,
    TeamSerializer,
    UserProfileSerializer,
    WorkoutSerializer,
)


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "users": request.build_absolute_uri("users/"),
            "teams": request.build_absolute_uri("teams/"),
            "activities": request.build_absolute_uri("activities/"),
            "leaderboard": request.build_absolute_uri("leaderboard/"),
            "workouts": request.build_absolute_uri("workouts/"),
        }
    )


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all().order_by("id")
    serializer_class = UserProfileSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all().order_by("id")
    serializer_class = TeamSerializer


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all().order_by("id")
    serializer_class = ActivitySerializer


class LeaderboardViewSet(viewsets.ModelViewSet):
    queryset = Leaderboard.objects.all().order_by("rank")
    serializer_class = LeaderboardSerializer


class WorkoutViewSet(viewsets.ModelViewSet):
    queryset = Workout.objects.all().order_by("id")
    serializer_class = WorkoutSerializer
