from rest_framework.serializers import ModelSerializer
from .models import Parcel, Product
from rest_framework import serializers
from common.serializers import GallerySerializer, GalleryImageSerializer
from common.models import Gallery


class ParcelBasicSerializer(ModelSerializer):
    product = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    has_current_production = serializers.SerializerMethodField()

    class Meta:
        model = Parcel
        fields = (
            "id",
            "name",
            "description",
            "product",
            "image",
            "has_current_production",
        )

    def get_product(self, parcel):
        return (
            parcel.current_history.product.name
            if parcel.current_history and parcel.current_history.product
            else None
        )

    def get_has_current_production(self, parcel):
        return parcel.current_history is not None

    def get_image(self, parcel):
        try:
            return (
                parcel.album.images.first().image.url
                if parcel.album
                and parcel.album.images.exists()
                and parcel.album.images.first().image is not None
                else None
            )
        except:
            return None


class RetrieveParcelSerializer(ModelSerializer):
    product = serializers.SerializerMethodField()
    establishment = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    productions_completed = serializers.SerializerMethodField()

    class Meta:
        model = Parcel
        exclude = ("album",)

    def get_product(self, parcel):
        return parcel.product.name if parcel.product else None

    def get_establishment(self, parcel):
        return parcel.establishment.name if parcel.establishment else None

    def get_image(self, parcel):
        try:
            return (
                parcel.album.images.first().image.url
                if parcel.album
                and parcel.album.images.exists()
                and parcel.album.images.first().image is not None
                else None
            )
        except:
            return None

    def get_images(self, parcel):
        try:
            return [
                image.image.url
                for image in parcel.album.images.all()
                if image.image is not None
            ]
        except:
            return []

    def get_productions_completed(self, parcel):
        return parcel.productions_completed


class CreateParcelSerializer(ModelSerializer):
    product = serializers.SerializerMethodField()
    album = GallerySerializer(required=False)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Parcel
        fields = "__all__"

    def get_product(self, parcel):
        return None

    def update(self, instance, validated_data):
        album_data = self.context.get("request").FILES
        if album_data:
            gallery = instance.album
            if gallery is None:
                gallery = Gallery.objects.create()
            for image_data in album_data.getlist("album[images]"):
                gallery_image = gallery.images.create(image=image_data)
                gallery_image.save()
            validated_data["album"] = gallery
        return super().update(instance, validated_data)

    def create(self, validated_data):
        album_data = self.context.get("request").FILES
        if album_data:
            gallery = Gallery.objects.create()
            for image_data in album_data.getlist("album[images]"):
                gallery_image = gallery.images.create(image=image_data)
                gallery_image.save()
            validated_data["album"] = gallery
        return super().create(validated_data)

    def get_image(self, parcel):
        try:
            return (
                parcel.album.images.first().image.url
                if parcel.album
                and parcel.album.images.exists()
                and parcel.album.images.first().image is not None
                else None
            )
        except:
            return None


class ProductListOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name"]


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "description", "image"]
