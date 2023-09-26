from django.shortcuts import render

# Create your views here.

from rest_framework import generics, permissions, viewsets, filters
from rest_framework.response import Response

from .models import Review
from .serializers import ReviewSerializer, ListReviewSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.OrderingFilter]

    def get_serializer_class(self):
        if self.action == "list":
            return ListReviewSerializer
        else:
            return ReviewSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        data["scan"] = data["scan_id"]
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)
