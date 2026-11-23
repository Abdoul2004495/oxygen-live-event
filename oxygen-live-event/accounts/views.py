# render builds a page from a template; redirect sends the visitor to another URL
from django.shortcuts import render, redirect

# The form we wrote in forms.py (the dot means "same folder")
from .forms import RegisterForm
from django.contrib import messages


# A view is a function that receives the request and returns a response
def register(request):
    # POST means the visitor submitted the form
    if request.method == "POST":
        # Fill the form with the data sent by the visitor (request.POST holds that data)
        form = RegisterForm(request.POST)
        # TEMPORARY DEBUG: prints every validation error in the terminal
        print(form.errors)
        # is_valid() runs every check: email format, unique email, matching passwords, password strength
        if form.is_valid():
            # Insert the member in the database and keep the created user
            user = form.save()
            # TEMPORARY DEBUG: proves the code reached this point
            print("SAVED:", user.email)
            # Stores a message shown once, on the next page the visitor sees
            messages.success(request, "Account created")
            # Send the visitor to the login page (URL name "login", created in Part 3)
            return redirect("login")
    # Otherwise it's a GET: the visitor just opened the page
    else:
        # An empty form to display
        form = RegisterForm()
    # Show the page, giving the form to the template under the name "form"
    return render(request, "accounts/register.html", {"form": form})
