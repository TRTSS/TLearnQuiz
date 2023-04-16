import logging
import math
import requests
from django.contrib.auth.models import User

import imgkit

from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.templatetags.static import static
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from TLearnQuiz.forms import NewUserForm
from .models import Quiz, QuizResult, XPBonus, Invite
from django.conf import settings as django_settings
import os
from django.template.loader import render_to_string


# Create your views here.
def play_quiz(request, quizId):
    logger = logging.getLogger('django')
    context = {'quizId': quizId}
    context['quizObj'] = Quiz.objects.filter(id=quizId).first()
    context['now'] = timezone.now()
    context['corrects'] = []
    context['sponsorTitle'] = context['quizObj'].quizSponsorTitle
    context['sponsorImage'] = context['quizObj'].quizSponsorImage
    print(context['sponsorTitle'])
    for i in Quiz.objects.filter(id=quizId).first().quizQuestions.all():
        context['corrects'].append(list(i.questionAnswers.all())[i.questionRightAnswerId].answerText)
        print(context['corrects'])
    logger.info("HI DEBUG CAT! MEOW!")
    return render(request, 'quiz.html', context)


def register_request(request):
    context = {}
    if request.method == "POST":
        print("Yammi data!")
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if request.GET.get('invitor') is not None:
                invitorIdR = int(request.GET.get('invitor'))
                bonus = XPBonus()
                bonus.xpAmount = 200
                bonus.recipient = request.user
                bonus.save()
                bonus = XPBonus()
                bonus.xpAmount = 100
                bonus.recipient = User.objects.get(id=invitorIdR)
                bonus.save()
                inv = Invite()
                inv.taker = request.user
                inv.inviter = User.objects.get(id=invitorIdR)
                inv.save()
                return redirect('/registed?invited=1')
            else:
                return redirect('/registed')
        else:
            messages.error(request, f'Не получилось вас зарегистрировать. email: {form}')
    context['invitor'] = None
    if request.GET.get('invitor') is not None:
        invitorId = int(request.GET.get('invitor'))
    if User.objects.filter(id=invitorId).exists():
        context['invitor'] = User.objects.get(id=invitorId)
    form = NewUserForm()
    context['register_form'] = form
    context['ip'] = get_client_ip(request)
    return render(request, 'newUser.html', context)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


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

@csrf_exempt
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

        totalScores, bonusScores = get_user_total_score(request.user)

        context['totalScoresPostfix'] = get_scores_postfix(totalScores + bonusScores)
        context['totalScores'] = totalScores + bonusScores

        if len(userResults) > 0:
            avScores = totalScores // len(userResults)
        else:
            avScores = 0
        postfix = get_scores_postfix(avScores)
        context['avScores'] = avScores
        context['avScoresPostfix'] = postfix

        bonuses = XPBonus.objects.filter(recipient=request.user)
        context['bonuses'] = []
        for b in bonuses:
            context['bonuses'].append(b)

        context['currentLevel'], context['currentXP'], context['xpNeed'] = get_user_level_data(
            totalScores + bonusScores)
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

    return level + 1, xp, xpNeed


def get_user_level_data_api(request):
    offset = 0
    if request.method == "GET":
        if request.GET.get('offset') is not None:
            offset = int(request.GET.get('offset'))
    userResults = QuizResult.objects.filter(quizUser=request.user)
    totalScores, bonusScores = get_user_total_score(request.user)
    level, xp, xpNeed = get_user_level_data((totalScores + bonusScores) - offset)
    return JsonResponse({'level': level, 'xp': xp, 'xpNeed': xpNeed})


def get_user_total_score(user):
    userResults = QuizResult.objects.filter(quizUser=user)
    totalScores = 0
    for res in userResults:
        totalScores += res.scores

    bonusScores = 0
    userBonuses = XPBonus.objects.filter(recipient=user)
    for bonus in userBonuses:
        bonusScores += bonus.xpAmount

    return totalScores, bonusScores


def get_stats_img(request):
    userResults = QuizResult.objects.filter(quizUser=request.user)
    totalScores, bonusScores = get_user_total_score(request.user)

    level, xp, xpNeed = get_user_level_data(totalScores + bonusScores)

    avScores = 0
    if len(userResults) > 0:
        avScores = round(totalScores / len(userResults))

    html = f"<script type='module' src='https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js'></script>" \
           f"<script nomodule src='https://unpkg.com/@google/model-viewer/dist/model-viewer-legacy.js'></script>" \
           f"<div class='holder'>" \
           f"<h1>Моя статистика TLearnQUIZ</h1><p>{request.user.username}</p>" \
           f"<div class='flex-holder'><div class='block-content'><p>Я участвовал в</p><h2>" \
           f"{len(userResults)}<span style='font-size: 16px'> квизах</span></h2></div><div " \
           f"class='block-content'><p>Мой суммарный счёт</p><h2>{totalScores + bonusScores}<span style='font-size: 16px'> очк" \
           f"{get_scores_postfix(totalScores + bonusScores)}</span></h2></div><div class='block-content'><p>Мой средний счёт</p><h2>{avScores}" \
           f"<span style='font-size: 16px'> очк{get_scores_postfix(avScores)}</span></h2></div></div>" \
           f"<div class='flex-holder'>" \
           f"<img src='http://zuvs.ru/static/imgs/cups/circleCup{str(1 + level // 10)}.png' style='position: realative; width: 50%;' alt='http://zuvs.ru/static/imgs/cups/circleCup{str(1 + level // 10)}.png'>" \
           f"<div>" \
           f"<h2>Участвуй в квизах вместе со мной!</h2>" \
           f"<p>Переходи в телеграмм канал: <i>t.me/tlearn_quiz</i> и участвуй в коротких ежедневных викторинах!</p>" \
           f"</div>" \
           f"</div>" \
           f"</div>"

    css = "@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@200;300;400;500;600;700;800&display" \
          "=swap'); body {background: #316BFF; color: white; padding: 30px; font-family: 'Manrope', sans-serif;} " \
          ".flex-holder {" \
          "display: flex;" \
          "flex-direction: row;" \
          "justify-content: space-between;" \
          "}" \
          ".block-content {" \
          "text-align: left !important;" \
          "padding: 25px;" \
          "background: rgba(255, 255, 255, 0.3);" \
          "border-radius: 30px;" \
          "margin: 10px;" \
          "}" \
          ".holder {" \
          "width: 800px;" \
          "}"

    HCTI_API_ENDPOINT = "https://hcti.io/v1/image"
    HCTI_API_USER_ID = 'ee866a44-9af0-4964-8911-fca5fc6f5904'
    HCTI_API_KEY = '99c853ac-de67-48a5-83f3-695c319a147c'

    data = {
        'html': html,
        'css': css
    }

    image = requests.post(url=HCTI_API_ENDPOINT, data=data, auth=(HCTI_API_USER_ID, HCTI_API_KEY))

    return JsonResponse({
        'url': image.json()['url']
    })


def get_stats_img_template(request):
    return render(request, 'statsDownloadTemplate.html', {})
