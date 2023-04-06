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
        if quiz.quizStartDate > timezone.now() and quiz.quizStartDate.date() == timezone.now().date():
            future.append(quiz)

    if len(future) > 0:
        message = f"Привет! Сегодня ({timezone.now().date()}) нас ждут следующие квизы:\n"
        for quiz in future:
            message += f"\n**{quiz.quizTitle}**\nНачало: {quiz.quizStartDate.time()})\n"
    else:
        message = "Привет! Сегодня отдыхаем - сегодня квизов не будет.";

    message += "\n(сообщение создано автоматически)"

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)

def SendQuizStartNotification ():
    apiToken = '5854080741:AAG5eK_jf5130SKO3dd8EgihxfKdIVki0vE'
    chatID = '-1001883219679'
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    allQuiz = Quiz.objects.all()
    for quiz in allQuiz:
        if quiz.quizStartDate.time() == timezone.now().time():
            message = f"КВИЗ '{quiz.quizTitle}' НАЧАЛСЯ:\n" \
                      f"Скорее заходи и участвуй!\n" \
                      f"Ссылка: http://zuvs.ru/quiz/{quiz.pk}"

            try:
                response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
                print(response.text)
            except Exception as e:
                print(e)