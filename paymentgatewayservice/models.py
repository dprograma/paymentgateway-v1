from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        user = self.create_user(email, name, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Users(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=90, blank=False, unique=False)
    email = models.EmailField(max_length=128, blank=False, unique=True)
    phone = models.CharField(max_length=16, null=True, blank=True)
    user_type = models.CharField(max_length=16, default="client")
    access_level = models.IntegerField(default=0)
    refcode = models.CharField(max_length=6, blank=False, unique=True)
    token = models.CharField(max_length=30, blank=False, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email


class USSDRequest(models.Model):
    phone = models.CharField(max_length=16, default="", blank=False)
    request_type = models.CharField(
        max_length=30,
        choices=[
            ("job_request", "Job Request"),
            ("worker_registration", "Worker Registration"),
        ],
        blank=False,
    )
    data = models.JSONField(default=dict, blank=False)
    status_code = models.IntegerField(
        default=0
    )  # 0=pending, 1=success (charged), 2=failed
    uuid_token = models.CharField(max_length=50, unique=True, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class USSDJobRequest(models.Model):
    request = models.ForeignKey(
        USSDRequest, on_delete=models.CASCADE, related_name="job_requests"
    )
    phone = models.CharField(max_length=16, default="", blank=False)
    title = models.CharField(max_length=100, default="", blank=False)
    location = models.CharField(max_length=100, default="", blank=False)
    status_code = models.IntegerField(
        default=0
    )  # 0=pending, 1=success (charged), 2=failed
    job_token = models.CharField(max_length=50, unique=True, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Create your models here.
class Jobs(models.Model):
    client = models.ForeignKey(
        Users, related_name="client_jobs", on_delete=models.CASCADE
    )
    worker = models.ForeignKey(
        Users, related_name="worker_jobs", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100)
    duration = models.CharField(max_length=50, default="")
    description = models.TextField(default="")
    prefer_date = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=100, default="")
    coordinates = models.JSONField(default=list)
    payment = models.JSONField(default=dict)
    status = models.IntegerField(default=0)
    worker_cord = models.JSONField(default=list)
    cancel_by = models.CharField(
        max_length=10,
        choices=[("worker", "Worker"), ("client", "Client")],
        null=True,
        blank=True,
    )
    cancel_comment = models.TextField(default="")
    worker_rating = models.IntegerField(default=0)
    worker_comment = models.TextField(default="")
    client_rating = models.IntegerField(default=0)
    client_comment = models.TextField(default="")
    created = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Job"
        verbose_name_plural = "Jobs"

    def __str__(self):
        return self.title


class Wallet(models.Model):
    user = models.OneToOneField(
        Users, related_name="wallet", on_delete=models.CASCADE, unique=True
    )
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    earning = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}'s Wallet"


class Transactions(models.Model):
    TRANSACTION_STATUS = [
        (-1, "Debit"),
        (0, "Pending"),
        (1, "Credited"),
        (2, "Cancel or Fail"),
    ]

    TRANSACTION_METHOD = [("cash", "Cash"), ("wallet", "Wallet")]

    user = models.ForeignKey(
        Users, related_name="transactions", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=128)
    body = models.TextField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.IntegerField(choices=TRANSACTION_STATUS)
    method = models.CharField(max_length=10, choices=TRANSACTION_METHOD)
    avatar = models.ImageField(upload_to="transaction_avatars/", null=True, blank=True)
    trans_response = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
