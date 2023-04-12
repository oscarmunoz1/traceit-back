from rest_framework import serializers

from .models import History, CommonEvent, ChemicalEvent, WeatherEvent, GeneralEvent


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonEvent
        fields = "__all__"


class ChemicalEventSerializer(EventSerializer):
    class Meta:
        model = ChemicalEvent
        fields = [
            "id",
            "type",
            "volume",
            "concentration",
            "time_period",
            "observation",
        ]


class WeatherEventSerializer(EventSerializer):
    class Meta:
        model = WeatherEvent
        fields = "__all__"


class GeneralEventSerializer(EventSerializer):
    class Meta:
        model = GeneralEvent
        fields = ["id", "name", "observation"]


class HistorySerializer(serializers.ModelSerializer):
    events = serializers.SerializerMethodField()
    certificate_percentage = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()

    class Meta:
        model = History
        fields = [
            "id",
            "start_date",
            "finish_date",
            "name",
            "description",
            "published",
            "events",
            "earning",
            "members",
            "certificate_percentage",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "certificate_percentage"]

    def get_events(self, history):
        return WeatherEventSerializer(
            history.history_weatherevent_events.all(), many=True
        ).data

    def get_certificate_percentage(self, history):
        return history.certificate_percentage

    def get_members(self, history):
        events = history.history_weatherevent_events.all()
        members = []
        for event in events:
            if event.created_by:
                members.append(
                    event.created_by.first_name + " " + event.created_by.last_name
                )
        return members[0:3]
