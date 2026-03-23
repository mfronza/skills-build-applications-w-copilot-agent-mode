from datetime import date

from django.core.management.base import BaseCommand
from pymongo import MongoClient

from octofit_tracker.models import Activity, Leaderboard, Team, UserProfile, Workout


class Command(BaseCommand):
    help = "Populate the octofit_db database with test data"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Clearing existing test data..."))
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        Leaderboard.objects.all().delete()
        Team.objects.all().delete()
        UserProfile.objects.all().delete()

        self.stdout.write(self.style.WARNING("Creating teams..."))
        team_marvel = Team.objects.create(
            name="Team Marvel",
            description="Earth's mightiest heroes training squad.",
        )
        team_dc = Team.objects.create(
            name="Team DC",
            description="Justice-inspired elite fitness league.",
        )

        self.stdout.write(self.style.WARNING("Creating user profiles..."))
        users = [
            UserProfile.objects.create(name="Spider-Man", email="spiderman@octofit.io", age=21, city="New York"),
            UserProfile.objects.create(name="Black Widow", email="blackwidow@octofit.io", age=34, city="New York"),
            UserProfile.objects.create(name="Superman", email="superman@octofit.io", age=35, city="Metropolis"),
            UserProfile.objects.create(name="Wonder Woman", email="wonderwoman@octofit.io", age=3000, city="Themyscira"),
        ]

        self.stdout.write(self.style.WARNING("Creating activities..."))
        Activity.objects.bulk_create(
            [
                Activity(
                    user=users[0],
                    activity_type="HIIT",
                    duration_minutes=45,
                    calories_burned=520,
                    date=date.today(),
                ),
                Activity(
                    user=users[1],
                    activity_type="Strength Training",
                    duration_minutes=60,
                    calories_burned=430,
                    date=date.today(),
                ),
                Activity(
                    user=users[2],
                    activity_type="Flying Sprints",
                    duration_minutes=30,
                    calories_burned=600,
                    date=date.today(),
                ),
                Activity(
                    user=users[3],
                    activity_type="Combat Conditioning",
                    duration_minutes=50,
                    calories_burned=480,
                    date=date.today(),
                ),
            ]
        )

        self.stdout.write(self.style.WARNING("Creating leaderboard entries..."))
        Leaderboard.objects.bulk_create(
            [
                Leaderboard(user=users[2], points=950, rank=1),
                Leaderboard(user=users[3], points=900, rank=2),
                Leaderboard(user=users[0], points=870, rank=3),
                Leaderboard(user=users[1], points=845, rank=4),
            ]
        )

        self.stdout.write(self.style.WARNING("Creating workout suggestions..."))
        Workout.objects.bulk_create(
            [
                Workout(user=users[0], title="Web Core Blast", difficulty="Intermediate", duration_minutes=35, focus_area="Core"),
                Workout(user=users[1], title="Stealth Endurance Circuit", difficulty="Advanced", duration_minutes=50, focus_area="Full Body"),
                Workout(user=users[2], title="Krypton Power Session", difficulty="Advanced", duration_minutes=40, focus_area="Strength"),
                Workout(user=users[3], title="Amazon Warrior Flow", difficulty="Intermediate", duration_minutes=45, focus_area="Mobility"),
            ]
        )

        # Keep memberships simple for the starter dataset via naming convention.
        team_memberships = {
            team_marvel.name: [users[0].name, users[1].name],
            team_dc.name: [users[2].name, users[3].name],
        }

        client = MongoClient("mongodb://localhost:27017")
        db = client["octofit_db"]
        db.octofit_tracker_userprofile.create_index("email", unique=True)

        self.stdout.write(self.style.SUCCESS("Database populated successfully."))
        self.stdout.write(
            self.style.SUCCESS(
                f"Team assignments: {team_memberships}"
            )
        )
