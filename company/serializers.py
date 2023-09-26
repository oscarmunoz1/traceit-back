from rest_framework.serializers import ModelSerializer
from .models import Company, Establishment
from rest_framework import serializers
from product.serializers import ParcelBasicSerializer


class EstablishmentSerializer(ModelSerializer):
    parcels = serializers.SerializerMethodField()

    class Meta:
        model = Establishment
        fields = (
            "id",
            "name",
            "description",
            "address",
            "city",
            "zone",
            "state",
            "image",
            "parcels",
            "image",
            "country",
        )

    def get_parcels(self, establishment):
        return ParcelBasicSerializer(establishment.parcels.all(), many=True).data


class DetailEstablishmentSerializer(ModelSerializer):
    class Meta:
        model = Establishment
        fields = "__all__"


class UpdateEstablishmentSerializer(ModelSerializer):
    class Meta:
        model = Establishment
        fields = "__all__"

    def to_representation(self, instance):
        return EstablishmentSerializer(instance).data


class RetrieveEstablishmentSerializer(ModelSerializer):
    parcels = serializers.SerializerMethodField()

    class Meta:
        model = Establishment
        fields = "__all__"

    def get_parcels(self, establishment):
        return ParcelBasicSerializer(establishment.parcels.all(), many=True).data


class EstablishmentChartSerializer(serializers.Serializer):
    series = serializers.ListField()
    options = serializers.SerializerMethodField()

    class Meta:
        model = Establishment
        fields = ["series", "options"]

    def get_options(self, establishment):
        period = self.context["period"]
        if period == "week":
            week_days = [
                "Sun",
                "Mon",
                "Tue",
                "Wed",
                "Thu",
                "Fri",
                "Sat",
            ]
            return [week_days[day - 1] for day in self.context["days"]]
        elif period == "month":
            return self.context["days"]
        elif period == "year":
            return [
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December",
            ]
        return []


class EstablishmentProductsReputationSerializer(serializers.Serializer):
    series = serializers.ListField()
    options = serializers.ListField()

    class Meta:
        model = Establishment
        fields = ["series", "options"]


class RetrieveCompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"

    establishments = serializers.SerializerMethodField()

    def get_establishments(self, company):
        return EstablishmentSerializer(company.establishment_set.all(), many=True).data


class CreateCompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        exclude = (
            "fiscal_id",
            "invitation_code",
        )
