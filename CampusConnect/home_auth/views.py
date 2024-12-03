from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from django.utils.crypto import get_random_string
from .models import CustomUser
from django.utils.text import slugify
from home_auth.models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import check_password
from .models import CustomUser
from home_auth.models import PasswordUpdate
def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST.get('role')  # Get role from the form (student, teacher, or admin)
        
        # Create the user
        user = CustomUser.objects.create_user(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        
        # Assign the appropriate role
        if role == 'student':
            user.is_student = True
        elif role == 'teacher':
            user.is_teacher = True
        elif role == 'admin':
            user.is_admin = True

        user.save()  # Save the user with the assigned role
        login(request, user)
        messages.success(request, 'Signup successful!')
        return redirect('index')  # Redirect to the index or home page
    return render(request, 'authentication/register.html')  # Render signup template



def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            
            # Redirect user based on their role
            if user.is_admin:
                return redirect('admin_dashboard')
            elif user.is_teacher:
                return redirect('faculty_dashboard')
            elif user.is_student:
                return redirect('student_dashboard')
            else:
                messages.error(request, 'Invalid user role')
                return redirect('index')  # Redirect to index in case of error
            
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'authentication/login.html')  # Render login template





def change_password_view(request):
    if request.method == "POST":
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")

        if not check_password(current_password, request.user.password):
            messages.error(request, "Current password is incorrect.")
            return HttpResponseRedirect(request.path_info)

        if len(new_password) < 3:
            messages.error(request, "New password must be at least 8 characters long.")
            return HttpResponseRedirect(request.path_info)

        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)

        messages.success(request, "Your password has been successfully updated.")
        return HttpResponseRedirect(request.path_info)
    

    return render(request, "school/profile.html", {"user": request.user})

def change_password_view_student(request):
    if request.method == "POST":
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")

        if not check_password(current_password, request.user.password):
            messages.error(request, "Current password is incorrect.")
            return HttpResponseRedirect(request.path_info)

        if len(new_password) < 3:
            messages.error(request, "New password must be at least 8 characters long.")
            return HttpResponseRedirect(request.path_info)

        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)

        messages.success(request, "Your password has been successfully updated.")
        return HttpResponseRedirect(request.path_info)
    

    return render(request, "school/profile_student.html", {"user": request.user})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')

def list_accounts_view(request):
    if request.method == "POST":
        if "delete_user_id" in request.POST:  # Handle delete operation
            user_id = request.POST["delete_user_id"]
            comment = request.POST.get("delete_comment", "").strip()
            if not comment:
                # Optional: Add error handling if the comment is missing
                messages.error(request, "Comment is required to delete a user.")
                return redirect("list_accounts")
            try:
                user = CustomUser.objects.get(id=user_id)
                # Optional: Log the comment or perform additional actions
                user.delete()
                messages.success(request, f"User {user.first_name} deleted successfully.")
            except CustomUser.DoesNotExist:
                messages.error(request, "User does not exist.")
            return redirect("list_accounts")

        # Process checkbox updates (existing logic)
        for key, value in request.POST.items():
            if key.startswith("authorize_"):
                user_id = key.split("_")[1]
                user = CustomUser.objects.get(id=user_id)
                user.is_active = value == "on"
                user.save()
            elif key.startswith("staff_"):
                user_id = key.split("_")[1]
                user = CustomUser.objects.get(id=user_id)
                user.is_staff = value == "on"
                user.save()
            elif key.startswith("superuser_"):
                user_id = key.split("_")[1]
                user = CustomUser.objects.get(id=user_id)
                user.is_superuser = value == "on"
                user.save()

    users = CustomUser.objects.all()
    return render(request, "authentication/list_accounts.html", {"users": users})
