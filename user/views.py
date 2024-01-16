from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import user_serializer
from rest_framework import status
from kafka import KafkaProducer

class Testing(APIView):
    def get(self, request):
        return Response("Welcome to microservices...")


class UserService(APIView):
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers='localhost:9092')
    def post(self, request):
        serializer =user_serializer(data=request.data)  # Use request.data instead of request.POST

        try:
            if serializer.is_valid():
                serializer.save()
                email = serializer.validated_data.get("email")
                print(email)
                self.producer.send("email", value=email.encode("utf-8"))
                return Response("User saved.", status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:  # Use the correct exception type and capture the exception object
            print(e)
            return Response("Error occurred.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            self.producer.close()


