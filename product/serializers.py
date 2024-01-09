from rest_framework.serializers import ModelSerializer
from .models import Parcel, Product
from rest_framework import serializers
from common.serializers import GallerySerializer
from common.models import Gallery


class ParcelBasicSerializer(ModelSerializer):
    product = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Parcel
        fields = ("id", "name", "description", "product", "image")

    def get_product(self, parcel):
        return (
            parcel.current_history.product.name
            if parcel.current_history and parcel.current_history.product
            else "No current production"
        )

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


class CreateParcelSerializer(ModelSerializer):
    product = serializers.SerializerMethodField()
    album = GallerySerializer(required=False, read_only=True)

    class Meta:
        model = Parcel
        fields = "__all__"

    def get_product(self, parcel):
        return "No current production"

    # def create(self, validated_data):
    #     images_data = self.context.get("request").data.get("images")
    #     parcel = Parcel.objects.create(**validated_data)
    #     if parcel.album is None:
    #         parcel.album = Gallery.objects.create()
    #     # for image_data in images_data:
    #     #     parcel.album.images.create(**image_data)
    #     return parcel

    #     # def update(self, instance, validated_data):
    #     print("entro si si si no no")
    #     print(self.context.get("request").FILES)
    #     print(self.context.get("request").__dict__)
    #     images_data = self.context.get("request").data.get("album")
    #     images_post = self.context.get("request").POST.get("album")
    #     image = self.context.get("request").FILES.get("album")
    #     data = self.context.get("request").data
    #     data2 = self.context.get("request").POST
    #     data3 = self.context.get("request").FILES

    #     print("images_data::::")
    #     print(images_data)
    #     print(validated_data)
    #     print(images_post)
    #     print(image)
    #     print(data)
    #     print(data2)
    #     print(data3)

    #     parcel = super().update(instance, validated_data)
    #     if parcel.album is None:
    #         print("album none entro si si si no no no")
    #         parcel.album = Gallery.objects.create()
    #     # for image_data in images_data:
    #     #     print("entro si si si no no no no")
    #     #     print(image_data)
    #     #     parcel.album.images.create(**image_data)
    #     return parcel


class ProductListOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name"]


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "description", "image"]
