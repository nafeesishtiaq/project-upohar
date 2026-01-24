from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, EmailTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.

User = get_user_model()

class RegisterView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = RegisterSerializer
  permission_classes = [permissions.AllowAny]

class LoginView(TokenObtainPairView):
  permission_classes = [AllowAny]
  serializer_class = EmailTokenObtainPairSerializer

class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("id_token")

        if not token:
            return Response({"error": "id_token required"}, status=400)

        try:
            info = id_token.verify_oauth2_token(
                token,
                google_requests.Request(),
                settings.GOOGLE_CLIENT_ID
            )
        except ValueError:
            return Response({"error": "Invalid Google token"}, status=400)

        email = info.get("email")

        if not email:
            return Response({"error": "Email not available"}, status=400)

        user, _ = User.objects.get_or_create(email=email)

        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })