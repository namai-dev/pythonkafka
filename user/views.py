from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import user_serializer, Transaction_Serializer, User_Account_Serializer
from rest_framework import status
from kafka import KafkaProducer
from .models import CustomUser, UserAccount, Transaction
from .my_functions import generate_account_number
import json

class Testing(APIView):
    def get(self, request):
        return Response("Welcome to microservices...")

class AuthService(APIView):
    def get(self, request):
        data = request.data
        username = data["email"]
        password = data["password"]
        user = CustomUser.objects.get(username=username)
        if user == null:
            return Response("Invalid credentials", status=status.HTTP_401_UNAUTHORIZED)
        user_pass = user.password
        if password != user_pass:
            return Response("Invalid credentials", status=status.HTTP_401_UNAUTHORIZED)


class UserService(APIView):
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers='localhost:9092')
    def post(self, request):
        serializer =user_serializer(data=request.data) 

        try:
            if serializer.is_valid():
                user = serializer.save()
                email = serializer.validated_data.get("email")
                account = UserAccount.objects.create(user=user, account_number=generate_account_number(), balance=0.0)
                account_details ={
                    "email":account.user.email,
                    "account_number":account.account_number,
                    "balance":account.balance
                }
                self.producer.send("account", value=json.dumps(account_details).encode("utf-8"))
                print(account)
                self.producer.send("email", value=email.encode("utf-8"))
                return Response("User saved.", status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:  
            print(e)
            return Response("Error occurred.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            self.producer.close()



class DepositView(APIView):
    def post(self, request):
        data = request.data
        deposit_amount = data["amount"]
        account_no = data["account_number"]
        account = UserAccount.objects.get(account_number=account_no)
        
        if not account:
            return Response("Invalid account..", status=status.HTTP_406_NOT_ACCEPTABLE)
        
        if deposit_amount <= 0:
            return Response("Invalid amount...", status=status.HTTP_406_NOT_ACCEPTABLE)
        
        account.balance += deposit_amount
        account.save()
        transaction = Transaction.objects.create(
            account=account,
            amount=deposit_amount,
            transaction_type=1,
            balance_after_transaction=account.balance
        )

        return Response("Deposit Successful. Check your email")




