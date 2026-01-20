from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

  class Meta:
    model = User
    fields = ['email', 'password']

  def create(self, validated_data):
    user = User.objects.create_user(
      email=validated_data['email'],
      password=validated_data['password']
    )
    return user

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
  username_field = 'email'

  def validate(self, attrs):
    data = super().validate(attrs)

    data['user'] = UserSerializer(self.user).data
    return data
  
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'email', 'date_joined', 'last_login']
