from django.contrib import admin
from django.urls import path
from . import views
from django.urls import path , include

urlpatterns = [
    path('', views.index,name="home"),

    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add_student/', views.add_student, name='add_student'),
    path('add_teacher/', views.add_teacher, name='add_teacher'),
    path('add_book/', views.add_book, name='add_book'),
    path('add_issued_book/', views.add_issued_book, name='add_issued_book'),
    path('add_homeimage/', views.add_homeimage, name='add_homeimage'),
    path('add_ejournal/', views.add_ejournal, name='add_ejournal'),
    


    path('book/', views.book, name="book"),
    path('login/', views.user_login, name='login'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path('ejournals/', views.ejournal_list, name='ejournal_list'),
    path('change_password/', views.change_password, name='change_password'),

   
  
    
]