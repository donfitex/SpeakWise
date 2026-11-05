from rest_framework import serializers

from .models import LearnerProfile

GOALS = [
    "daily-life",
    "pronunciation",
    "diction",
    "grammar",
    "interviews",
    "work",
    "public-speaking",
    "listening",
]


class ProfileSerializer(serializers.ModelSerializer):
    goals = serializers.ListField(child=serializers.ChoiceField(choices=GOALS), max_length=8)
    daily_minutes = serializers.IntegerField(min_value=5, max_value=120)

    class Meta:
        model = LearnerProfile
        fields = [
            "id",
            "display_name",
            "first_language",
            "level",
            "goals",
            "pronunciation_model",
            "daily_minutes",
        ]
        read_only_fields = ["id"]
