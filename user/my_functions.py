from .models import UserAccount
import random

def generate_account_number():
    while True:
        account_number = random.randint(10**11, 10**12 - 1)

        if not UserAccount.objects.filter(account_number=account_number).exists():
            return account_number


