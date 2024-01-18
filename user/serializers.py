from rest_framework.serializers import ModelSerializer
from  .models import CustomUser, UserAccount, Transaction


class user_serializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password', 'username']

class User_Account_Serializer(ModelSerializer):
    class Meta:
        model = UserAccount
        fields = "__all__"


class Transaction_Serializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"