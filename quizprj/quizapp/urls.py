from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    
    path('home/', views.home, name='home'),
    path('user-home/', views.user_home, name='user_home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    
    path('start/', views.start, name='start'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('question/', views.add_question, name='add_question'),
    
    path('addChoice/<int:p_id>/', views.add_choice, name='addChoice'),
    # path('editchoice/<int:choice_id>/', views.choice_edit, name='editchoice'),
    # path('choicedelete/<int:choice_id>/',views.choice_delete, name='choicedelete'),
    
    path('edit/<int:p_id>/', views. edit_question, name='editQuestion'),
    # path('delete/<int:p_id>/', views.polls_delete, name='deleteQuestion'),
    
    path('submission-result/<int:attempted_question_pk>/', views.submission_result, name='submission_result'),
    
    
    path('timer/', views.timer, name='timer'),
    
    
    
    
]