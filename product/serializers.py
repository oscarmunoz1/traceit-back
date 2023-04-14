from rest_framework.serializers import ModelSerializer
from .models import Parcel
from rest_framework import serializers


class ParcelBasicSerializer(ModelSerializer):
    product = serializers.SerializerMethodField()

    class Meta:
        model = Parcel
        fields = ("id", "name", "description", "image", "product")

    def get_product(self, parcel):
        return parcel.product.name if parcel.product else None


class RetrieveParcelSerializer(ModelSerializer):
    product = serializers.SerializerMethodField()
    establishment = serializers.SerializerMethodField()

    class Meta:
        model = Parcel
        fields = "__all__"

    def get_product(self, parcel):
        return parcel.product.name if parcel.product else None

    def get_establishment(self, parcel):
        return parcel.establishment.name if parcel.establishment else None


class CreateParcelSerializer(ModelSerializer):
    class Meta:
        model = Parcel
        fields = "__all__"
