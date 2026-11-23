# Base blueprint for a user (AbstractUser) and base class for the object that creates users (BaseUserManager)
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Tools to describe database tables: models.Model, CharField, EmailField, ...
from django.db import models


# The manager: the object behind User.objects.create_user(...) and createsuperuser
class UserManager(BaseUserManager):
    """Teaches Django how to create users who log in with an email."""

    # Records this manager inside migration files (recommended for custom user managers)
    use_in_migrations = True

    # Creates a normal user; extra_fields collects any other named values (phone, first_name, ...)
    def create_user(self, email, password=None, **extra_fields):
        # Refuse to create an account without an email
        if not email:
            raise ValueError("The email address is required")
        # Lowercases the domain part: Ali@GMAIL.COM -> Ali@gmail.com
        email = self.normalize_email(email)
        # Builds a User object in memory (not in the database yet)
        user = self.model(email=email, **extra_fields)
        # Hashes the password (one-way scramble), never stores the real one
        user.set_password(password)
        # Writes the user as a new row in the database
        user.save(using=self._db)
        # Gives the created user back to whoever called the function
        return user

    # Creates an admin account with all permissions
    def create_superuser(self, email, password=None, **extra_fields):
        # setdefault: set the value only if nobody provided one
        extra_fields.setdefault("is_staff", True)        # can enter /admin/
        extra_fields.setdefault("is_superuser", True)    # has every permission
        extra_fields.setdefault("role", "admin")         # our own role column

        # Safety checks: reject the creation if someone forced these to False
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        # Reuse create_user so the real work (normalize, hash, save) lives in one place
        return self.create_user(email, password, **extra_fields)


# The custom User model: becomes the table accounts_user
class User(AbstractUser):
    class Role(models.TextChoices):
        CLIENT = "client", "Client"
        ADMIN = "admin", "Admin"

    # Allowed values for the gender column (same pattern as Role)
    class Gender(models.TextChoices):
        MALE = "male", "Male"        # NAME = "value stored in DB", "label shown to humans"
        FEMALE = "female", "Female"

    username = None
    email = models.EmailField("email address", unique=True)
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.CLIENT)

    # Gender column: limited to the Gender choices; blank=True so it may stay empty
    gender = models.CharField(max_length=10, choices=Gender.choices, blank=True)
    # City column: text up to 100 characters, may stay empty
    city = models.CharField(max_length=100, blank=True)
    # Country column: same idea
    country = models.CharField(max_length=100, blank=True)

    # Which column identifies the user at login
    USERNAME_FIELD = "email"
    # Extra questions asked by createsuperuser (email and password are always asked)
    REQUIRED_FIELDS = []

    # Plug in our manager so User.objects.create_user uses our version
    objects = UserManager()

    # How a user is displayed as text (in the admin list, for example)
    def __str__(self):
        return self.email