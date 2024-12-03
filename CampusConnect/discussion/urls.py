from django.urls import path
from . import views

urlpatterns = [
    # General URLs
    path('thread/<int:thread_id>/', views.thread_detail, name='thread_detail'),
    path('threads/', views.thread_list, name='thread_list'),
    path('studentthreads/', views.thread_list_student, name='thread_list_student'),
    path('thread/<int:thread_id>/upvote/', views.upvote_thread, name='upvote_thread'),
    path('thread/<int:thread_id>/vote/', views.vote_thread, name='vote_thread'),
    path('create-thread/', views.create_thread, name='create_thread'),

    # Student-specific URLs
    path('student/thread/<int:thread_id>/', views.thread_detail_student, name='thread_detail_student'),
    path('student/threads/', views.thread_list_student, name='thread_list_student'),
]
