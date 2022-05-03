from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "name"]


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def save(self, request):
        email = self.validated_data.get("email")
        password = self.validated_data.get("password")

        new_user = User.objects.create_user(email, password, is_active=True)

        return new_user
