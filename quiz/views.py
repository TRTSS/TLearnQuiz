import logging
import math

from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.templatetags.static import static
from django.utils import timezone

from TLearnQuiz.forms import NewUserForm
from .models import Quiz, QuizResult


# Create your views here.
def play_quiz(request, quizId):
    logger = logging.getLogger('django')
    context = {'quizId': quizId}
    context['quizObj'] = Quiz.objects.filter(id=quizId).first()
    context['now'] = timezone.now()
    context['corrects'] = []
    print("hel")
    for i in Quiz.objects.filter(id=quizId).first().quizQuestions.all():
        context['corrects'].append(list(i.questionAnswers.all())[i.questionRightAnswerId].answerText)
        print(context['corrects'])
    logger.info("HI DEBUG CAT! MEOW!")
    return render(request, 'quiz.html', context)


def register_request(request):
    if request.method == "POST":
        print("Yammi data!")
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/registed')
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
        results = QuizResult.objects.filter(quizRef=Quiz.objects.filter(id=quizId).first()).all().order_by('-scores')[
                  :10]
        board = {
            'all': {},
            'player': {}
        }
        for index, value in enumerate(results):
            board['all'][index] = {}
            board['all'][index]["username"] = value.quizUser.username
            board['all'][index]["scores"] = value.scores
        if request.user.is_authenticated and QuizResult.objects.filter(quizRef=Quiz.objects.filter(id=quizId).first(),
                                                                       quizUser=request.user).exists():
            playerRes = QuizResult.objects.get(quizRef=Quiz.objects.filter(id=quizId).first(), quizUser=request.user)
            board['player'] = {
                'username': playerRes.quizUser.username,
                'scores': playerRes.scores
            }
        return JsonResponse({'ok': True, 'data': board})
    else:
        return JsonResponse({'ok': False})


def bot_connection(request):
    return render(request, 'botConnect.html', {})


def get_effects_sandbox(request):
    return render(request, 'effectssandbox.html', {})


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


def get_user_registed(request):
    return render(request, 'registDone.html', {})


def user_stats(request):
    context = {}
    if request.user.is_authenticated:
        userResults = QuizResult.objects.filter(quizUser=request.user)
        context['quizCount'] = len(userResults)

        totalScores = 0
        for res in userResults:
            totalScores += res.scores

        context['totalScoresPostfix'] = get_scores_postfix(totalScores)
        context['totalScores'] = totalScores

        avScores = totalScores // len(userResults)
        postfix = get_scores_postfix(avScores)
        context['avScores'] = avScores
        context['avScoresPostfix'] = postfix

        context['currentLevel'], context['currentXP'], context['xpNeed'] = get_user_level_data(totalScores)
        context['leagueBadge'] = static(f"3d/cups/circleCup{1 + context['currentLevel'] // 10}.gltf")

    return render(request, 'statistic.html', context)


def get_scores_postfix(scores):
    postfix = 'a'
    if scores % 10 in [0, 5, 6, 7, 8, 9]:
        postfix = 'ов'
    elif scores % 10 == 1:
        postfix = 'о'

    return postfix


def get_user_level_data(scores):
    level = 0
    xp = scores
    xpNeed = 100
    while xp >= xpNeed:
        xp -= xpNeed
        level += 1
        xpNeed *= 1.03
        xpNeed = math.ceil(xpNeed)

    return level+1, xp, xpNeed


def get_user_level_data_api(request):
    userResults = QuizResult.objects.filter(quizUser=request.user)
    totalScores = 0
    for res in userResults:
        totalScores += res.scores
    level, xp, xpNeed = get_user_level_data(totalScores)
    return JsonResponse({'level': level, 'xp': xp, 'xpNeed': xpNeed})
