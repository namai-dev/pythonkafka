from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.hashers import make_password
from .constants import TRANSACTION_TYPE_CHOICE

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', "username"]

    def save(self, *args, **kwargs):
        # Hash the password before saving
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

class UserAccount(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    account_number = models.IntegerField(max_length=12)
    balance = models.FloatField(default=0.0)

    def __str__(self):
        return str(self.account_number)
    


class Transaction(models.Model):
    account = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    amount = models.FloatField()
    transaction_type = models.PositiveSmallIntegerField(
        choices = TRANSACTION_TYPE_CHOICE
    )
    balance_after_transaction = models.FloatField(max_length=12)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.account)
    

    class META:
        ordering = ["time_stamp"]


