from rest_framework import serializers
from .models import Review


class ListReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    production = serializers.SerializerMethodField()
    date = serializers.DateTimeField(format="%d/%m/%Y", required=False)

    class Meta:
        model = Review
        fields = "__all__"

    def get_user(self, review):
        return review.user.get_full_name()

    def get_production(self, review):
        return (
            review.production.product.name
            + " - "
            + review.production.parcel.name
            + " - "
            + review.production.finish_date.strftime("%d/%m/%Y")
        )


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
