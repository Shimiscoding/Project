from django.contrib import admin
from django.urls import path, include
from . import views
from .views import profile_view, profile_view_student
from school.views import library_view, library_view_student


urlpatterns = [
    path('', views.index, name="index"),
    path('notification/mark-as-read/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('notification/clear-all/', views.clear_all_notification, name="clear_all_notification"),
    
    # Dashboard URLs
    path('student-dashboard/', views.studentdashboard, name='student_dashboard'),
    path('admin-dashboard/', views.admindashboard, name='admin_dashboard'),
    path('faculty-dashboard/', views.facultydashboard, name='faculty_dashboard'),
    
    
    # Announcement URLs
    path('announcements/', views.announcement_view, name='announcements'),
    path('create-announcement/', views.create_announcement, name='create_announcements'),
    path('announcements/<uuid:id>/', views.announcement_detail, name='announcement_detail'),
    path('admin/announcement/<uuid:id>/', views.admin_announcement_detail, name='admin_announcement_detail'),
    path('admin/announcements/', views.announcement_view_admin, name='admin_announcements'),
    path('admin/announcement/<uuid:id>/edit/', views.edit_announcement, name='edit_announcement'),
    path('admin/announcement/<uuid:id>/delete/', views.delete_announcement, name='delete_announcement'),

    # Others URL
    path('profile/<str:username>/', profile_view, name='profile'),
    path('profile/student/<str:username>//', views.profile_view_student, name='profile_student'),
    path('student/library/', library_view_student, name='library_student'), 
    path('library/', library_view, name='library'),
    
    
    
    
]
