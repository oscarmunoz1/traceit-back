from rest_framework.serializers import ModelSerializer
from .models import Parcel, Product
from rest_framework import serializers
from common.serializers import GallerySerializer, GalleryImageSerializer
from common.models import Gallery
from users.models import User
from users.serializers import BasicUserSerializer
from django.conf import settings


class ParcelBasicSerializer(ModelSerializer):
    product = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    has_current_production = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()

    class Meta:
        model = Parcel
        fields = (
            "id",
            "name",
            "description",
            "product",
            "image",
            "has_current_production",
            "members",
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
            if not parcel.album or not parcel.album.images.exists():
                return None
            
            image = parcel.album.images.first().image
            if not image:
                return None
            print('image.url\n\n\n\n\n\n\n\n\n');
            print(image.url);
            request = self.context.get('request')
            print('request\n\n\n\n\n\n\n\n\n');
            print(request);
            if request:
                return request.build_absolute_uri(image.url)
            return image.url
        except Exception as e:
            print(f"Error getting image: {str(e)}")
            return None

    def get_members(self, parcel):
        members_ids = []
        for history in parcel.histories.all():
            members_ids += history.get_involved_users()
        members_ids = list(set(members_ids))
        members = User.objects.filter(id__in=members_ids)[0:2]
        return BasicUserSerializer(members, many=True).data


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
            if not parcel.album:
                return []
            
            request = self.context.get('request')
            return [
                request.build_absolute_uri(image.image.url) if request else image.image.url
                for image in parcel.album.images.all()
                if image.image is not None
            ]
        except Exception as e:
            print(f"Error getting images: {str(e)}")
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

            request = self.context.get('request')

            print('request.build_absolute_uri(parcel.album.images.first().image.url)\n\n\n\n\n\n\n\n\n');
            print(                request.build_absolute_uri(parcel.album.images.first().image.url)
                if parcel.album
                and parcel.album.images.exists()
                and parcel.album.images.first().image is not None
                else None);
            return (
                request.build_absolute_uri(parcel.album.images.first().image.url)
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
