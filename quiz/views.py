import json

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate

from TLearnQuiz.forms import NewUserForm

from .models import Quiz, QuizResult


# Create your views here.
def play_quiz(request, quizId):
    context = {'quizId': quizId}
    context['quizObj'] = Quiz.objects.filter(id=quizId).first()
    context['now'] = timezone.now()
    context['corrects'] = []
    print("hel")
    for i in Quiz.objects.filter(id=quizId).first().quizQuestions.all():
        context['corrects'].append(list(i.questionAnswers.all())[i.questionRightAnswerId].answerText)
        print(context['corrects'])
    return render(request, 'quiz.html', context)


def register_request(request):
    if request.method == "POST":
        print("Yammi data!")
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Вы успешно зарегистрировались!")
        else:
            messages.error(request, f'Не получилось вас зарегистрировать. email: {form}')
    form = NewUserForm()
    return render(request, 'newUser.html', context={'register_form': form})


def login_request(request):
    context = {}
    if request.GET.get('auto', '') == 'logout':
        logout(request)
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if request.GET.get('redirect', '') != '':
                    return redirect(request.GET.get('redirect', ''))
                else:
                    return render(request, 'index.html', {})
            else:
                context['error'] = "Неверный логин или пароль"
        else:
            context['error'] = "Неверный логин или пароль"
    form = AuthenticationForm()
    context["login_form"] = form
    return render(request, "login.html", context)


# API
def check_access_to_quiz(request):
    print("access")
    if request.method == "POST":
        quizId = request.POST.get('quizId')
        quiz = Quiz.objects.filter(id=quizId).first()
        if timezone.now() < quiz.quizStartDate:
            return JsonResponse({'ok': False, 'verbose': 'Квиз еще не начался'})
        else:
            return JsonResponse({'ok': True})


def send_quiz_result(request):
    if request.method == "POST":
        quizId = request.POST.get('quizId')
        scores = request.POST.get('scores')
        if QuizResult.objects.filter(quizRef=Quiz.objects.filter(id=quizId).first(), quizUser=request.user).exists():
            return JsonResponse({'ok': False, 'verbose': 'Вы уже проходили этот квиз'})
        else:
            res = QuizResult()
            res.quizRef = Quiz.objects.filter(id=quizId).first()
            res.quizUser = request.user
            res.scores = scores
            res.save()
            return JsonResponse({'ok': True})


def get_quiz_leaders(request):
    if request.method == "POST":
        quizId = request.POST.get('quizId')
        results = QuizResult.objects.filter(quizRef=Quiz.objects.filter(id=quizId).first()).all().order_by('-scores')
        board = {}
        for index, value in enumerate(results):
            board[index] = {}
            board[index]["username"] = value.quizUser.username
            board[index]["scores"] = value.scores
        return JsonResponse({'ok': True, 'data': board})
    else:
        return JsonResponse({'ok': False})


def bot_connection(request):
    return render(request, 'botConnect.html', {})


def get_index(request):
    context = {}
    allQuiz = Quiz.objects.all()

    now = timezone.now()

    context['futureQuiz'] = []
    context['activeQuiz'] = []
    context['passedQuiz'] = []
    for quiz in allQuiz:
        if now < quiz.quizStartDate:
            context['futureQuiz'].append(quiz)
        elif quiz.quizStartDate <= now <= quiz.quizEndDate:
            context['activeQuiz'].append(quiz)
        else:
            context['passedQuiz'].append(quiz)
    return render(request, 'index.html', context)
