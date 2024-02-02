from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm, RegistrationForm
from django.contrib.auth import authenticate, logout, login as dj_login
from django.contrib.auth import logout as django_logout
from .models import QuizProfile, Question, AttemptedQuestion, Choice
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse
from .forms import QuestionForm, ChoiceAddForm, EditQuestionForm
from django.contrib import messages
from datetime import datetime

import calendar
import time


# Create your views here.

# User = get_user_model()


def home(request):
    context = {}
    return render(request, 'quiz/home.html', context=context)


@login_required()
def user_home(request):
    print(request.user.is_superuser)
    if request.user.is_superuser:
            context = {
                'superuser' : request.user.is_superuser
            }
            
    context = {}
    
    return render(request, 'quiz/user_home.html', context=context)

def timer(request):
    question = Question.objects.all()
    #  context = {
    #     'question' : question 
    # }
    # for ques in question:
        
    context = {
        'question' : question 
    }
    
    return render(request, 'quiz/timer.html', context)
    

def login(request):
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        dj_login(request, user)
        return redirect('/user-home')
    return render(request, 'quiz/login.html', {"form": form, "title": title})


def register(request):
    title = "Create account"
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    else:
        form = RegistrationForm()

    context = {'form': form, 'title': title}
    return render(request, 'quiz/registration.html', context=context)


def logout(request):
    # logout(request)
    django_logout(request)
    messages.success(request, "Logged Out",  extra_tags='alert alert-success alert-dismissible fade show')
    return redirect('/home')


@login_required()
def start(request):
    
    quiz_profile, created = QuizProfile.objects.get_or_create(user=request.user)
    
    import datetime
  
    current_time = datetime.datetime.now()
  
    timestamp = current_time.timestamp()
    
    date_time = datetime.datetime.fromtimestamp(timestamp)
    str_date_time = date_time.strftime("%d-%m-%Y, %H:%M:%S")   
    print("timestamp:-", str_date_time)
    
    
    if request.method == 'POST':
        
        question_pk = request.POST.get('question_pk')
        

        attempted_question = quiz_profile.attempts.select_related('question').get(question__pk=question_pk)
        
        choice_pk = request.POST.get('choice_pk')
        
        try:
            selected_choice = attempted_question.question.choices.get(pk=choice_pk)
            
        except ObjectDoesNotExist:
            raise Http404

        quiz_profile.evaluate_attempt(attempted_question, selected_choice)

        return redirect('quiz:submission_result', attempted_question.id)

    else:

        question = quiz_profile.get_new_question()
        
        if question is not None:
            quiz_profile.create_attempt(question)
       
        context = {
            'question': question,
            
        }

        return render(request, 'quiz/start.html', context=context)


def dashboard(request):

    # top_quiz_profiles = QuizProfile.objects.order_by('-total_score')[:500]

    # total_count = top_quiz_profiles.count()
    
    top_quiz_profiles = QuizProfile.get_rankings()[:500]
    total_count = top_quiz_profiles.count()

    context = {
        'top_quiz_profiles': top_quiz_profiles,
        'total_count': total_count,
    }
    return render(request, 'quiz/dashboard.html', context=context)


@login_required()
def submission_result(request, attempted_question_pk):
    
    attempted_question = get_object_or_404(AttemptedQuestion, pk=attempted_question_pk)
    
    context = {
        'attempted_question': attempted_question,
    }

    return render(request, 'quiz/submission_result.html', context=context)


@login_required()
def add_question(request):
    
        # if not request.user.is_superuser:
        #     return HttpResponse('The user is not superuser')
        
        if request.method == 'POST':
            
            form = QuestionForm(request.POST)
            
            if form.is_valid:
                question = form.save(commit=False)
                question.owner = request.user
                question.save()
                
                #retrive e the question id
                latest_question = Question.objects.latest('id')
                question_id = latest_question.id
                return redirect(f'/addChoice/{question_id}')
            
                #return redirect('/home')
        else:
            form = QuestionForm()
            context = {
                'form': form,
            }
            return render(request, 'quiz/create_question.html', context)
        
        
def edit_question(request, p_id):
    
    # if not request.user.is_superuser:
    #         return HttpResponse('The user is not superuser')
    
    question_instance = get_object_or_404(Question, pk=p_id)
    
    if request.method == 'POST':
        form = EditQuestionForm(request.POST, instance=question_instance)
        if form.is_valid:
            form.save()
            messages.success(request, "Question Updated successfully.",
                             extra_tags='alert alert-success alert-dismissible fade show')
            return redirect("/home")

    else:
        form = EditQuestionForm(instance=question_instance)

    return render(request, "quiz/edit_question.html", {'form': form, 'poll': question_instance})
        
        
        
@login_required
def add_choice(request, p_id):
    question = get_object_or_404(Question, pk=p_id)
    

    if request.method == 'POST':
        form = ChoiceAddForm(request.POST)
        if form.is_valid:
            
            new_choice = form.save(commit=False)
            
            new_choice.question = question
            
            new_choice.save()
            messages.success(
                request, "Choice added successfully.", extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('quiz:editQuestion', question.id)
    else:
        form = ChoiceAddForm()
    context = {
        'form': form,
    }
    return render(request, 'quiz/add_choice.html', context)


