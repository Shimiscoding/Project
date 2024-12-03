#views.py

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Notification, Comment
from django.http import HttpResponseForbidden
from student.models import Student
from teacher.models import Teacher
from django.shortcuts import get_object_or_404
from home_auth.models import CustomUser
from django.contrib import messages
from discussion.models import Category  
from events.models import Event
from datetime import datetime
from discussion.models import Thread



def index(request):
    return render(request, "authentication/login.html")

def admindashboard(request):
    # Fetch all students and count them
    students = Student.objects.all()
    categories = Category.objects.all()  # Fetch categories
    teachers = Teacher.objects.all()
    student_count = students.count()
    teacher_count = teachers.count()
    student_slug = Student.objects.first().slug
    # Fetch unread notifications for the current user and count them
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
    unread_notification_count = unread_notifications.count()

    # Fetch all event notifications and count them
    event_notifications = Notification.objects.filter(category='events')
    event_count = event_notifications.count()

    # Fetch today's date
    today = datetime.today()
    
    # Fetch all events happening today and order by start_time
    events_today = Event.objects.filter(start_time__date=today.date()).order_by('start_time')

    # Fetch all academic notifications and count them
    academic_notifications = Notification.objects.filter(category='academics')
    academic_count = academic_notifications.count()

    # Fetch all threads and count them
    threads = Thread.objects.all()[:4]
    thread_count = threads.count()

    # Prepare context with required data
    context = {
        'students': students,
        'teachers': teachers,
        'student_count': student_count,
        'teacher_count': teacher_count,
        'student_slug': student_slug,
        'unread_notifications': unread_notifications,
        'unread_notification_count': unread_notification_count,
        'categories': categories,  # Pass categories to the template
        'event_count': event_count,  # Include the event count
        'academic_count': academic_count,  # Include the academic count
        'events_today': events_today,  # Pass today's events to the template
        'threads': threads,  # Pass the forum threads to the template
        'thread_count': thread_count,  # Pass the thread count
    }

    # Render the dashboard template with context
    return render(request, "admin/admin-dashboard.html", context)


def studentdashboard(request):
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
    unread_notification_count = unread_notifications.count()
      # Fetch all threads and count them
    threads = Thread.objects.all()[:4]
    thread_count = threads.count()
     # Fetch today's date
    today = datetime.today()
    
    # Fetch all events happening today and order by start_time
    events_today = Event.objects.filter(start_time__date=today.date()).order_by('start_time')
    context = {
        'unread_notifications': unread_notifications,
        'unread_notification_count': unread_notification_count,
        'threads': threads,  # Pass the forum threads to the template
        'thread_count': thread_count,
        'events_today': events_today, 

    }
    return render(request, "students/student-dashboard.html", context)

def facultydashboard(request):
     # Fetch all students and count them
    students = Student.objects.all()
    categories = Category.objects.all()  # Fetch categories
    teachers = Teacher.objects.all()
    student_count = students.count()
    teacher_count = teachers.count()
    student_slug = Student.objects.first().slug
    # Fetch unread notifications for the current user and count them
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
    unread_notification_count = unread_notifications.count()

    # Fetch all event notifications and count them
    event_notifications = Notification.objects.filter(category='events')
    event_count = event_notifications.count()

    # Fetch today's date
    today = datetime.today()
    
    # Fetch all events happening today and order by start_time
    events_today = Event.objects.filter(start_time__date=today.date()).order_by('start_time')

    # Fetch all academic notifications and count them
    academic_notifications = Notification.objects.filter(category='academics')
    academic_count = academic_notifications.count()

    # Fetch all threads and count them
    threads = Thread.objects.all()[:4]
    thread_count = threads.count()

    # Prepare context with required data
    context = {
        'students': students,
        'teachers': teachers,
        'student_count': student_count,
        'teacher_count': teacher_count,
        'student_slug': student_slug,
        'unread_notifications': unread_notifications,
        'unread_notification_count': unread_notification_count,
        'categories': categories,  # Pass categories to the template
        'event_count': event_count,  # Include the event count
        'academic_count': academic_count,  # Include the academic count
        'events_today': events_today,  # Pass today's events to the template
        'threads': threads,  # Pass the forum threads to the template
        'thread_count': thread_count,  # Pass the thread count
    }

    # Render the dashboard template with context
    return render(request, "teachers/teacher-dashboard.html", context)


def mark_notification_as_read(request):
    if request.method == 'POST':
        notifications = Notification.objects.filter(user=request.user, is_read=False)
        notifications.update(is_read=True)
        return JsonResponse({'status': 'success'})
    return HttpResponseForbidden()

def clear_all_notification(request):
    if request.method == "POST":
        notification = Notification.objects.filter(user=request.user)
        notification.delete()
        return JsonResponse({'status': 'success'})
    return HttpResponseForbidden

def create_announcement(request):
    # Default values for title, message, and category
    title = ''
    message = ''
    category = ''
    event_date = None  # Initialize event_date

    # Check user authorization
    if not (request.user.is_staff or Teacher.objects.filter(user=request.user).exists()):
        return HttpResponseForbidden("You are not allowed to create announcements.")
    
    if request.method == 'POST':
        title = request.POST.get('title', '')
        message = request.POST.get('message', '')
        category = request.POST.get('category', 'General')
        file = request.FILES.get('file')
        event_date = request.POST.get('event_date')  # Get the event date

        if not title:
            title = 'No title'
        if not message:
            message = 'No message provided'

        # Create the notification
        notification = Notification.objects.create(
            user=request.user,
            title=title,
            message=message,
            category=category,
            file=file,
            is_read=False
        )

        # If the category is "events", save the event date
        if category == 'events' and event_date:
            # Optionally validate the date here (e.g., ensure it's not in the past)
            notification.event_date = event_date
            notification.save()

        messages.success(request, "Announcement created successfully!")
        return redirect('admin_announcements')

    return render(request, 'school/create_announcements.html', {
        'title': title,
        'message': message,
        'category': category,
    })



def profile_view(request, username):
    # Fetch the user profile based on the username in the URL
    user = get_object_or_404(CustomUser, username=username)
    
    # Determine the user type (e.g., student, teacher, or admin)
    user_type = (
        "student" if user.is_student else
        "teacher" if user.is_teacher else
        "admin"
    )

    # Render the profile template with the relevant data
    return render(request, "school/profile.html", {"user_type": user_type, "profile_data": user})

def profile_view_student(request, username):
    # Fetch the user profile based on the username in the URL
    user = get_object_or_404(CustomUser, username=username)
    
    # Determine the user type (e.g., student, teacher, or admin)
    user_type = (
        "student" if user.is_student else
        "teacher" if user.is_teacher else
        "admin"
    )

    # Render the profile template with the relevant data
    return render(request, "school/profile_student.html", {"user_type": user_type, "profile_data": user})

# =================================================================
# STUDENT 
# =================================================================

def announcement_detail(request, id):
    announcement = get_object_or_404(Notification, id=id)
    comments = announcement.comments.all()

    # Check if the user is authenticated and handle comment submission
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Comment.objects.create(
                notification=announcement,
                user=request.user,
                text=text
            )
            return redirect('announcement_detail', id=id)

    context = {
        'announcement': announcement,
        'comments': comments,
    }

    # If the announcement has a file, include it in the context
    if announcement.file:
        context['file_url'] = announcement.file.url

    return render(request, 'school/announcement_detail.html', context)

def announcement_view(request):
    announcements = Notification.objects.all()  # You may want to filter or limit announcements
    return render(request, 'school/announcements.html', {'announcements': announcements})




def library_view(request):
    # Filter announcements by "Academics" category
    academic_announcements = Notification.objects.filter(category='academics').order_by('-created_at')

    return render(request, 'school/library.html', {
        'academic_announcements': academic_announcements,
    })

def library_view_student(request):
    # Filter announcements by "Academics" category
    academic_announcements = Notification.objects.filter(category='academics').order_by('-created_at')

    return render(request, 'school/library_student.html', {
        'academic_announcements': academic_announcements,
    })


# ========================================================================================================================
# ADMIN
# ========================================================================================================================

def announcement_view_admin(request):
    announcements = Notification.objects.all()  # You may want to filter announcements for admin view
    return render(request, 'school/admin_announcements.html', {'announcements': announcements})



def admin_announcement_detail(request, id):
    announcement = get_object_or_404(Notification, id=id)

    # Check if the user is either an admin or a teacher
    if not (request.user.is_staff or Teacher.objects.filter(user=request.user).exists()):
        return HttpResponseForbidden("You are not authorized to edit or delete announcements.")

    comments = announcement.comments.all()

    if request.method == 'POST':
        # Check if it's a comment submission
        if 'text' in request.POST:
            text = request.POST.get('text')
            if text:
                Comment.objects.create(
                    notification=announcement,
                    user=request.user,
                    text=text
                )
                return redirect('admin_announcement_detail', id=id)

        # Handle announcement edit
        elif 'edit' in request.POST:  
            announcement.title = request.POST.get('title', announcement.title)
            announcement.message = request.POST.get('message', announcement.message)
            announcement.category = request.POST.get('category', announcement.category)
            announcement.save()
            return redirect('admin_announcement_detail', id=announcement.id)

        # Handle announcement deletion
        elif 'delete' in request.POST:  
            announcement.delete()
            return redirect('announcement_view_admin')  # Redirect to the admin announcements list after deletion

    return render(request, 'school/admin_announcement_detail.html', {
        'announcement': announcement,
        'comments': comments,
    })

def edit_announcement(request, id):
    announcement = get_object_or_404(Notification, id=id)

    if not (request.user.is_staff or Teacher.objects.filter(user=request.user).exists()):
        return HttpResponseForbidden("You are not authorized to edit announcements.")

    if request.method == 'POST':
        title = request.POST.get('title', announcement.title)
        message = request.POST.get('message', announcement.message)
        category = request.POST.get('category', announcement.category)

        announcement.title = title
        announcement.message = message
        announcement.category = category
        announcement.save()

        return redirect('admin_announcement_detail', id=announcement.id)

    return render(request, 'school/edit_announcement.html', {'announcement': announcement})

# Delete Announcement View
def delete_announcement(request, id):
    announcement = get_object_or_404(Notification, id=id)

    if not (request.user.is_staff or Teacher.objects.filter(user=request.user).exists()):
        return HttpResponseForbidden("You are not authorized to delete announcements.")

    announcement.delete()
    return redirect('admin_announcements')  # Redirect to the announcements list after deletion