from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.event_list, name='event_list'),  # List all events
    path('student/events/<int:pk>/', views.event_detail_student, name='event_detail_student'),  
    path('student/events/', views.event_list_student, name='event_list_student'),  # List all events
    path('events/<int:pk>/', views.event_detail, name='event_detail'), 
    path('calendar/', views.calendar_view, name='calendar_view'), 
    path('create/', views.create_event, name='create_event'), 
]
