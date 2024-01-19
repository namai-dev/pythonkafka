from rest_framework.serializers import ModelSerializer
from  .models import CustomUser, UserAccount, Transaction
from rest_framework import serializers


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
    


class TransactionSerializer(serializers.ModelSerializer):
    transaction_type = serializers.CharField(source='get_transaction_type_display', read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'

    def get_transaction_type_display(self, obj):
        if obj.transaction_type == Transaction.DEPOSIT:
            return "Deposit"
        elif obj.transaction_type == Transaction.WITHDRAW:
            return "Withdrawal"
        elif obj.transaction_type == Transaction.SEND_MONEY:
            return "Send Money"
        else:
            return "Unknown"