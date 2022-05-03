from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import UserDetailSerializer

User = get_user_model()


class UserViewSet(ModelViewSet):
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()
    lookup_field = "id"

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = UserDetailSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)
