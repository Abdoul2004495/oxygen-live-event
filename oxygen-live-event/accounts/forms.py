# Django's ready-made sign-up form: it already handles password1, password2 and password validation
from django.contrib.auth.forms import UserCreationForm

# Our custom User model
from .models import User


# Our form inherits everything from UserCreationForm
class RegisterForm(UserCreationForm):
    # Meta holds settings about the form itself
    class Meta:
        # Which model this form creates objects for
        model = User
        # Fields the visitor fills in (password1 and password2 are added automatically by UserCreationForm)
        # No "username" (it was removed) and no "role" (visitors must not choose it)
        fields = ("first_name", "last_name", "email", "phone", "gender", "city", "country")