from .serializers import BasicUserSerializer
from .models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from django.middleware import csrf

from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny
from rest_framework import status, generics
from rest_framework.decorators import action, permission_classes, api_view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from .serializers import LoginSerializer, RegisterSerializer, MeSerializer
from rest_framework.views import APIView
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]
    serializer_class = BasicUserSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["date_joined"]
    ordering = ["-date_joined"]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()

    def get_object(self):
        lookup_field_value = self.kwargs[self.lookup_field]
        obj = User.objects.get(id=lookup_field_value)
        self.check_object_permissions(self.request, obj)

        return obj

    @action(detail=False, methods=["get"])
    def me(self, request, pk=None):
        serializer = MeSerializer(request.user, context={"request": request})
        return Response(serializer.data)


@permission_classes([AllowAny])
def verify_email(self, request, *args, **kwargs):
    user = self.get_object_or_404(User, pk=request.data.get("email"))
    code = request.data.get("code")
    if not code:
        return Response(
            {"error": "Verification code is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if user.is_verified:
        return Response(
            {"error": "User is already verified"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if user.verification_code.code != code:
        return Response(
            {"error": "Verification code is invalid"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    user.verification_code.delete()
    user.is_verified = True
    user.save()
    return Response(status=status.HTTP_200_OK)


class LoginViewSet(viewsets.ModelViewSet, TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        response = Response(serializer.validated_data, status=status.HTTP_200_OK)

        response.set_cookie(
            key="access",
            value=serializer.validated_data["access"],
            expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )
        response.set_cookie(
            key="refresh",
            value=serializer.validated_data["refresh"],
            expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )
        response.set_cookie(
            key="logged_in",
            value=True,
            expires=timedelta(seconds=20),
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            httponly=False,
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )
        csrf.get_token(request)
        return response


class RegistrationViewSet(viewsets.ModelViewSet, TokenObtainPairView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        res = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        return Response(
            {
                "user": serializer.data,
                "refresh": res["refresh"],
                "token": res["access"],
            },
            status=status.HTTP_201_CREATED,
        )


class CustomTokenRefreshView(TokenRefreshView):
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.COOKIES)
        try:
            if not serializer.is_valid():
                return Response({"error": "Token is invalid or expired"}, status=400)
            refresh_token = RefreshToken(serializer.validated_data["refresh"])
        except Exception as e:
            return Response({"error": str(e)}, status=400)

        response = Response(serializer.validated_data, status=status.HTTP_200_OK)
        response.set_cookie(
            key="access",
            value=serializer.validated_data["access"],
            expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )
        response.set_cookie(
            key="refresh",
            value=serializer.validated_data["refresh"],
            expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )
        response.set_cookie(
            key="logged_in",
            value=True,
            expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            httponly=False,
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )
        csrf.get_token(request)
        return response


class APILogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        response = Response({"data": {"user": "ok"}}, status=status.HTTP_200_OK)
        response.delete_cookie(
            "access",
            domain=settings.SIMPLE_JWT["AUTH_COOKIE_DOMAIN"],
            path="/",
            samesite="None",
        )
        response.delete_cookie(
            "refresh",
            domain=settings.SIMPLE_JWT["AUTH_COOKIE_DOMAIN"],
            path="/",
            samesite="None",
        )
        response.delete_cookie(
            "logged_in",
            domain=settings.SIMPLE_JWT["AUTH_COOKIE_DOMAIN"],
            path="/",
            samesite="None",
        )
        return response
