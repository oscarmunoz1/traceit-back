from rest_framework import permissions, viewsets
from django.shortcuts import get_object_or_404

from company.models import Company


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.is_superuser
        )


class AuthPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class UserWorksInCompany(permissions.BasePermission):
    def has_permission(self, request, view):
        from users.models import WorksIn

        if not request.user.is_authenticated:
            return False
        if view.company is None and view.kwargs.get("company_pk") is None:
            # We're at the Company level and don't have a Company pk (list or create actions)
            # In this cases we have no company to check the user against, so we allow access and let
            # AuthPermission check
            return True
        if WorksIn.objects.filter(user=request.user, company=view.company).exists():
            return True
        return False


class CompanyNestedViewSet(viewsets.GenericViewSet):
    permission_classes = [IsSuperUser | (UserWorksInCompany & AuthPermission)]
    perms_map = {}
    company = None
    model = None

    def initial(self, request, *args, **kwargs):
        lookup_field = "company_pk"
        company_pk = kwargs.get(lookup_field)
        if company_pk is not None:
            self.company = get_object_or_404(Company, pk=company_pk)
        if establishment_pk := kwargs.get("establishment_pk"):
            self.establishment = get_object_or_404(
                self.company.establishment_set.all(), pk=establishment_pk
            )

        super().initial(request, *args, **kwargs)
