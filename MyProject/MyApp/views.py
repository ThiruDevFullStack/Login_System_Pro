from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
def sign_up(request):
    errors = {}

    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not first_name:
            errors['first_name'] = "First name is required."
        if not last_name:
            errors['last_name'] = "Last name is required."
        if not email:
            errors['email'] = "Email is required."
        if not username:
            errors['username'] = "Username is required."
        if not password:
            errors['password'] = "Password is required."

        if errors:
            return render(request, "MyAppHTML/sign_up.html", {'errors': errors})

        # Check if a user with the provided username already exists
        user = User.objects.filter(username=username)

        if user.exists():
            errors['username'] = "Username already taken!"
            return render(request, "MyAppHTML/sign_up.html", {'errors': errors})

        # Create a new User object with the provided information
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username
        )


        user.set_password(password)
        user.save()

        messages.success(request, 'You have signed up successfully!')
        return redirect('/sign_in/')

    return render(request,"MyAppHTML/sign_up.html")

def sign_in(request):

    try:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            if not username or not password:
                # Display an error message if either is missing
                messages.error(request, 'Please Enter All Data')
                return redirect('/sign_in/')

            # Check if a user with the provided username exists
            if not User.objects.filter(username=username).exists():
                # Display an error message if the username does not exist
                messages.error(request, 'Invalid Username')
                return redirect('/sign_in/')

            # Authenticate the user with the provided username and password
            user = authenticate(username=username, password=password)

            if user is None:
                # Display an error message if authentication fails (invalid password)
                messages.error(request, "Invalid Password")
                return redirect('/sign_in/')
            else:
                # Log in the user and redirect to the home page upon successful login
                login(request, user)
                return HttpResponse("""
                        <script>
                        alert("You are successfully signed in !");
                        window.location.href = 'http://127.0.0.1:8000/';
                    </script>
                                    """)
    except Exception as e:
        return HttpResponse("""
                <script>
                alert("An error occurred! Please try again");
                window.history.back()
                </script>
                """)
    return render(request,"MyAppHTML/sign_in.html")

def forget_password(request):

    try:
        if request.method == 'POST':
            name_email = request.POST.get('name_email')
            password = request.POST.get('password')

            if not name_email or not password:
                # Display an error message if either is missing
                messages.error(request, 'Please Enter All Data')
                return redirect('/forget_password/')

            user = User.objects.filter(Q(username=name_email) | Q(email=name_email)).first()

            if user is None:
                # Display an error message if no user found
                messages.error(request, 'Invalid Username or Email')
                return redirect('/forget_password/')
                # Reset the user's password
            user.password = make_password(password)  # Encrypt the new password
            user.save()

            # Display success message and redirect to login page
            messages.success(request, 'Password reset successful. Please log in.')
            return redirect('/sign_in/')



    except Exception as e:
        return HttpResponse("""
                              <script>
                              alert("An error occurred! Please try again.");
                              window.history.back()
                              </script>
                    """)

    return render(request,"MyAppHTML/forget_password.html")