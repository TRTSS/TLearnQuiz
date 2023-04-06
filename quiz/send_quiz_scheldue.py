import requests

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate

from TLearnQuiz.forms import NewUserForm

from .models import Quiz, QuizResult

apiToken = '5854080741:AAG5eK_jf5130SKO3dd8EgihxfKdIVki0vE'
chatID = '-1001883219679'
apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

future = []

allQuiz = Quiz.objects.all()
for quiz in allQuiz:
    if quiz.quizStartDate > timezone.now():
        future.append(quiz)

message = f"Future: {len(future)}"

try:
    response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
    print(response.text)
except Exception as e:
    print(e)
