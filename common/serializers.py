from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Gallery, GalleryImage


class GalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryImage
        fields = "__all__"


class GallerySerializer(serializers.ModelSerializer):
    images = GalleryImageSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = Gallery
        fields = "__all__"

    def create(self, validated_data):
        images_data = self.context.get("request").data.get("images")
        gallery = Gallery.objects.create(**validated_data)
        if images_data is not None:
            for image_data in images_data:
                GalleryImage.objects.create(gallery=gallery, image=image_data)
        return gallery

    def update(self, instance, validated_data):
        images_data = self.context.get("request").data.get("images")
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        if images_data is not None:
            for image_data in images_data:
                GalleryImage.objects.create(gallery=instance, image=image_data)
        return instance
