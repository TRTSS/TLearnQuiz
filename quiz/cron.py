import logging

import requests
from django.utils import timezone

from quiz.models import Quiz


def SendQuizScheldue():
    apiToken = '5854080741:AAG5eK_jf5130SKO3dd8EgihxfKdIVki0vE'
    chatID = '-1001883219679'
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    future = []

    allQuiz = Quiz.objects.all()
    for quiz in allQuiz:
        if quiz.quizStartDate > timezone.now():
            future.append(quiz)

    message = f"Предстоящие сегодня квизы\n:"
    for quiz in future:
        message += f"\n**{quiz.quizTitle}**\nНачало: {quiz.quizStartDate} ({quiz.quizStartDate.day})\n"

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)
