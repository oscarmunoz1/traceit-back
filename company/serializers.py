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
        )

    def get_parcels(self, establishment):
        return ParcelBasicSerializer(establishment.parcels.all(), many=True).data


class DetailEstablishmentSerializer(ModelSerializer):
    class Meta:
        model = Establishment
        fields = "__all__"


class CreateEstablishmentSerializer(ModelSerializer):
    class Meta:
        model = Establishment
        fields = "__all__"


class RetrieveEstablishmentSerializer(ModelSerializer):
    class Meta:
        model = Establishment
        fields = "__all__"

    parcels = serializers.SerializerMethodField()

    def get_parcels(self, establishment):
        return ParcelBasicSerializer(establishment.parcels.all(), many=True).data


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
