from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    class Meta:
        db_table = "Users"


class UserFollower(models.Model):
    follower = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.follower} takip ediyor {self.following}"

    class Meta:
        db_table = "User_Followers"
        unique_together = ("follower", "following")


class FavoriteBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey("books.Book", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.book}"

    class Meta:
        db_table = "Favorite_Books"
        unique_together = ("user", "book")


class ReadingProgress(models.Model):
    STATUS_CHOICES = [
        ('reading', 'Reading'),
        ('finished', 'Finished'),
        ('paused', 'Paused'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey("books.Book", on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    last_read = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.book} - {self.status}"

    class Meta:
        db_table = "Reading_Progress"
        unique_together = ("user", "book")

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username}"

    class Meta:
        ordering = ['timestamp']



