from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, filters, mixins
from .models import Parcel, Product
from .serializers import (
    RetrieveParcelSerializer,
    CreateParcelSerializer,
    ProductListSerializer,
    ProductListOptionsSerializer,
)
from history.serializers import HistorySerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class ParcelViewSet(viewsets.ModelViewSet):
    queryset = Parcel.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]

    def get_serializer_class(self):
        if (
            self.action == "create"
            or self.action == "update"
            or self.action == "partial_update"
        ):
            return CreateParcelSerializer
        return RetrieveParcelSerializer

    @action(detail=True, methods=["get"])
    def current_history(self, request, pk=None):
        parcel = self.get_object()
        current_history = parcel.current_history
        return Response(HistorySerializer(current_history).data)

    @action(detail=True, methods=["get"])
    def history(self, request, pk=None):
        parcel = self.get_object()

        histories = parcel.histories.filter(published=True)
        if parcel.current_history is not None:
            return Response(
                HistorySerializer(
                    histories.exclude(id=parcel.current_history.id), many=True
                ).data
            )
        return Response(HistorySerializer(histories, many=True).data)

    @action(detail=True, methods=["post"])
    def finish_history(self, request, pk=None):
        parcel = self.get_object()
        history_data = request.data
        history = parcel.finish_current_history(history_data)
        if history is not None:
            return Response(HistorySerializer(history).data)
        return Response(status=400)

    def partial_update(self, request, pk=None):
        parcel = self.get_object()
        print("entro 12,3,45,5,4,3,")
        print(request.FILES)
        print(request.POST)
        print(request.GET)
        print(request.data)
        # print(request.FILES.getlist("images"))
        parcel_data = request.data
        serializer = CreateParcelSerializer(
            parcel, data=parcel_data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            album = parcel_data.get("album")
            print(album)
            print("ese fue el album")
            if album is not None:
                print("entro")
                for image_data in album.get("images"):
                    print(image_data)
                    parcel.album.images.create(
                        image=image_data.get("image"), gallery=parcel.album
                    )
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class ProductsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
