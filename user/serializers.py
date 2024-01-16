from rest_framework.serializers import ModelSerializer
from  .models import CustomUser


class user_serializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password', 'username']