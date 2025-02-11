from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.models import auth
from django.contrib import messages
from .models import CustomUser
import re

CustomUser = get_user_model()


def check_password_strength(password):
    if len(password) < 8:
        return False

    if not re.search(r"[A-Z]", password):
        return False

    if not re.search(r"[a-z]", password):
        return False

    if not re.search(r"[0-9]", password):
        return False
        
    return True


def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email_input = request.POST.get("email_input")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
        elif not check_password_strength(password):
            messages.error(request, "Password is not strong enough")
        elif CustomUser.objects.filter(email=email_input).exists():
            messages.error(request, "Email Taken")
        elif CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username Taken")
        else:
            user = CustomUser.objects.create_user(
                username=username,
                email=email_input,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            if user is not None:
                messages.success(request, "Account created successfully!")
                return redirect("signin")
            else:
                messages.error(
                    request, "Failed to create account. Please try again later."
                )

        return render(
            request,
            "registrations/signup.html",
            {
                "username": username,
                "email_input": email_input,
                "first_name": first_name,
                "last_name": last_name,
            },
        )
    else:
        return render(request, "registrations/signup.html")


@login_required(login_url="signin")
def logout(request):
    auth.logout(request)
    return redirect("signin")


def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("post_list")
        else:
            messages.error(request, "Invalid Credentials")
            return render(request, "registrations/signin.html", {"username": username})
    else:
        return render(request, "registrations/signin.html")


def profile(request, pk):
    user_profile = get_object_or_404(CustomUser, pk=pk)
    return render(request, "profile.html", {"user_profile": user_profile})


@login_required(login_url="signin")
def settings(request):
    user_profile = request.user

    if request.method == "POST":
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")
        bio = request.POST.get("bio", "")

        user_profile.first_name = first_name
        user_profile.last_name = last_name
        user_profile.bio = bio

        if "profile_picture" in request.FILES:
            profile_picture = request.FILES["profile_picture"]
            user_profile.profile_picture = profile_picture

        user_profile.save()

        return redirect("profile", user_profile.pk)

    return render(request, "settings.html", {"user_profile": user_profile})