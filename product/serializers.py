from rest_framework.serializers import ModelSerializer
from .models import Parcel, Product
from rest_framework import serializers
from common.serializers import GallerySerializer
from common.models import Gallery


class ParcelBasicSerializer(ModelSerializer):
    product = serializers.SerializerMethodField()
    # image = serializers.SerializerMethodField()

    class Meta:
        model = Parcel
        fields = ("id", "name", "description", "product")

    def get_product(self, parcel):
        return (
            parcel.current_history.product.name
            if parcel.current_history and parcel.current_history.product
            else "No current production"
        )


class RetrieveParcelSerializer(ModelSerializer):
    product = serializers.SerializerMethodField()
    establishment = serializers.SerializerMethodField()

    class Meta:
        model = Parcel
        exclude = ("album",)

    def get_product(self, parcel):
        return parcel.product.name if parcel.product else None

    def get_establishment(self, parcel):
        return parcel.establishment.name if parcel.establishment else None


class CreateParcelSerializer(ModelSerializer):
    product = serializers.SerializerMethodField()
    album = GallerySerializer(required=False, read_only=True)

    class Meta:
        model = Parcel
        fields = "__all__"

    def get_product(self, parcel):
        return "No current production"

    def create(self, validated_data):
        print("entro si si si")
        images_data = self.context.get("request").data.get("images")
        parcel = Parcel.objects.create(**validated_data)
        if parcel.album is None:
            parcel.album = Gallery.objects.create()
        for image_data in images_data:
            parcel.album.images.create(**image_data)
        return parcel

    def update(self, instance, validated_data):
        print("entro si si si no no")
        print(self.context.get("request").__dict__)
        images_data = self.context.get("request").data.get("album")
        images_post = self.context.get("request").POST.get("album")
        image = self.context.get("request").FILES.get("album")
        data = self.context.get("request").data
        print("images_data::::")
        print(images_data)
        print(validated_data)
        print(images_post)
        print(image)
        print(data)

        parcel = super().update(instance, validated_data)
        if parcel.album is None:
            print("album none entro si si si no no no")
            parcel.album = Gallery.objects.create()
        # for image_data in images_data:
        #     print("entro si si si no no no no")
        #     print(image_data)
        #     parcel.album.images.create(**image_data)
        return parcel


class ProductListOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name"]


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "description", "image"]
