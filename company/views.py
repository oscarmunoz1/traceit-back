from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import (
    RetrieveCompanySerializer,
    CreateCompanySerializer,
    CreateEstablishmentSerializer,
    RetrieveEstablishmentSerializer,
)
from .models import Company
from users.models import WorksIn


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.OrderingFilter]

    def get_serializer_class(self):
        if self.action == "create":
            return CreateCompanySerializer
        return RetrieveCompanySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        company = serializer.save()
        company.save()
        WorksIn.objects.create(user=request.user, company=company, role="FA")
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EstablishmentViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.OrderingFilter]

    def get_serializer_class(self):
        if self.action == "create":
            return CreateEstablishmentSerializer
        return RetrieveEstablishmentSerializer
