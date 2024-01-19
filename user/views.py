from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import user_serializer, Transaction_Serializer, User_Account_Serializer, TransactionSerializer
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
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers='localhost:9092')
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

class WithdrawView(APIView):
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers='localhost:9092')
    def post(self, request):
        data = request.data
        withdrawal_amount = data["amount"]
        account_no = data["account_number"]
        
        try:
            account = UserAccount.objects.get(account_number=account_no)
        except UserAccount.DoesNotExist:
            return Response("Invalid account..", status=status.HTTP_406_NOT_ACCEPTABLE)
        
        if withdrawal_amount <= 0:
            return Response("Invalid amount...", status=status.HTTP_406_NOT_ACCEPTABLE)
        
        if account.balance < withdrawal_amount:
            return Response("Insufficient funds...", status=status.HTTP_406_NOT_ACCEPTABLE)
        
        account.balance -= withdrawal_amount
        account.save()  # Save the updated balance

        transaction = Transaction.objects.create(
            account=account,
            amount=-withdrawal_amount,  # Negative amount for withdrawal
            transaction_type=2,  # Assuming 2 is the code for withdrawal
            balance_after_transaction=account.balance
        )

        return Response("Withdrawal Successful. Check your email")



class TransactionHistoryView(APIView):
    def get(self, request, account_number):
        try:
            transactions = Transaction.objects.filter(account__account_number=account_number)
        except Transaction.DoesNotExist:
            return Response("No transactions found for the specified account.", status=status.HTTP_404_NOT_FOUND)
        
        serialized_transactions = TransactionSerializer(transactions, many=True)
        return Response(serialized_transactions.data)



class SendMoneyView(APIView):
    def post(self, request):
        data = request.data
        sender_account_no = data.get("sender_account_number")
        receiver_account_no = data.get("receiver_account_number")
        amount = data.get("amount")

        try:
            sender_account = UserAccount.objects.get(account_number=sender_account_no)
            receiver_account = UserAccount.objects.get(account_number=receiver_account_no)
        except UserAccount.DoesNotExist:
            return Response("Invalid sender or receiver account.", status=status.HTTP_406_NOT_ACCEPTABLE)

        if amount <= 0:
            return Response("Invalid amount.", status=status.HTTP_406_NOT_ACCEPTABLE)

        if sender_account.balance < amount:
            return Response("Insufficient funds.", status=status.HTTP_406_NOT_ACCEPTABLE)

        sender_account.balance -= amount
        receiver_account.balance += amount

        sender_account.save()
        receiver_account.save()

        sender_transaction = Transaction.objects.create(
            account=sender_account,
            amount=-amount,
            transaction_type=3,
            balance_after_transaction=sender_account.balance
        )

        receiver_transaction = Transaction.objects.create(
            account=receiver_account,
            amount=amount,
            transaction_type=3,
            balance_after_transaction=receiver_account.balance
        )

        serialized_sender_transaction = TransactionSerializer(sender_transaction).data
        serialized_receiver_transaction = TransactionSerializer(receiver_transaction).data

        return Response({
            "message": "Money sent successfully.",
            "sender_transaction": serialized_sender_transaction,
            "receiver_transaction": serialized_receiver_transaction
        })





