from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from .models import Parcel
from .serializers import RetrieveParcelSerializer
from history.serializers import HistorySerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class ParcelViewSet(viewsets.ModelViewSet):
    queryset = Parcel.objects.all()
    serializer_class = RetrieveParcelSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]

    @action(detail=True, methods=["get"])
    def current_history(self, request, pk=None):
        parcel = self.get_object()
        current_history = parcel.current_history
        return Response(HistorySerializer(current_history).data)

    @action(detail=True, methods=["get"])
    def history(self, request, pk=None):
        parcel = self.get_object()

        histories = parcel.histories.all()
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
