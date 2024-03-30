from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .helpers import *
import uuid
from .models import *
User = get_user_model()


# Create your views here.

def Signup(request):
    try:
        if request.method == 'POST':
            fullname = request.POST.get('fullname')
            email = request.POST.get('email')
            number = request.POST.get('number')
            newpassword = request.POST.get('newpassword')
            confpassword = request.POST.get('confpassword')

            if newpassword != confpassword:
                messages.error(request, "Passwords do not match")
                return redirect('Signup')

            # Check if the email or phone number already exists in the database
            if User.objects.filter(email=email).exists() or User.objects.filter(number=number).exists():
                messages.error(request, "Email or phone number already exists")
                return redirect('Signup')

            # Create the user if email and phone number are unique
            my_user = User.objects.create_user(email=email, password=newpassword)
            my_user.fullname = fullname
            my_user.number = number
            my_user.save()
            messages.success(
                request, "Account created successfully. Please log in.")
            return redirect('Login')

        return render(request, 'hacktivist/sign-up.html')
        
    except Exception as e:
        print("-------- Unexpected Error: -------", e)
        messages.error(request, "Unexpected Error. Try again later")
        return redirect('Signup')



def Login(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, email=email, password=password)
            print("-------- Print user ---------", user)

            if user is not None:
                login(request, user)
                return redirect('Index')
            else:
                messages.error(request, "Invalid username or password")
                return redirect('Login')
        return render(request, 'hacktivist/login.html')

    except Exception as e:
        print("------- Unexpected Error -----:", e)
        messages.error(request, "Unexpected Error, Try again later")
        return redirect('Login')


def Logout(request):
    logout(request)
    return redirect('Signup')


def ForgetPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        # Check if a user with the provided email exists
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "No email found")
            return redirect('ForgetPassword')

        # Generate a unique token
        token = str(uuid.uuid4())

        # Update the forget_password_token field in the user's profile
        try:
            profile_obj, created = Profile.objects.get_or_create(user=user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
        except Exception as e:
            messages.error(request, "An error occurred. Try again.")
            return redirect('ForgetPassword')

        # Send forget password email
        send_forget_password_mail(user_obj.email, token)

        messages.success(request, "An email has been sent")
        return redirect('ForgetPassword')

    return render(request, 'hacktivist/forget.html')


def ChangePassword(request, token):
    context = {}
    try:
        profile_obj = Profile.objects.get(forget_password_token=token)

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            user_id = request.POST.get('user_id')

            if not user_id:
                messages.error(request, 'No user found')
                return redirect(f'/change-password/{token}/')

            if new_password != confirm_password:
                messages.error(request, 'Passwords do not match')
                # return redirect(f'/change-password/{token}/')
                return redirect(reverse('ChangePassword', kwargs={'token': token}))

            user_obj = User.objects.get(id=user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            messages.success(
                request, 'Password changed successfully. Log in now.')
            return redirect('Login')

        context = {'user_id': profile_obj.user.id, 'token': token}

    except Profile.DoesNotExist:
        messages.error(request, 'Invalid reset token.')
        return redirect('ForgetPassword')

    except Exception as e:
        messages.error(request, 'Please try again later.')
        print("Error:", e)  # Print exception for debugging

    return render(request, 'hacktivist/change-password.html', context)


# ======================================= ! Don't change this code ! ===============================
# This is the main code : Got this from CHATGPT
# def ForgetPassword(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')

#         if User.objects.filter(email=email).exists():
#             user_obj = User.objects.get(email=email)
#             token = str(uuid.uuid4())
#             send_forget_password_mail(email, token)
#             messages.success(request, "An email has been sent with instructions to reset your password.")
#             return redirect('ForgetPassword')
#         else:
#             messages.error(request, "No user found with that email address.")
#             return redirect('ForgetPassword')
#     return render(request, 'hacktivist/forget.html')


# This is the debugging code that is used when user not recieved any pasword reset link
# send_mail(
#     'Subject of Test Email',
#     'Body of the test email.',
#     'arpanbera1212@gmail.com',
#     ['me.arpan122@gmail.com'],
#     fail_silently=False
# )
