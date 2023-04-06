import datetime
import logging

import requests
from django.utils import timezone

from quiz.models import Quiz
from aiogram import Bot, Dispatcher, executor, types

BOT_API_TOKEN = "5854080741:AAG5eK_jf5130SKO3dd8EgihxfKdIVki0vE"

bot = Bot(token=BOT_API_TOKEN)
dp = Dispatcher(bot)
chatID = '-1001883219679'

def SendQuizScheldue():
    apiToken = '5854080741:AAG5eK_jf5130SKO3dd8EgihxfKdIVki0vE'
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
        bot.send_message(chat_id=chatID, text=message)
    except Exception as e:
        print(e)


def SendQuizStartNotification():
    apiToken = '5854080741:AAG5eK_jf5130SKO3dd8EgihxfKdIVki0vE'
    chatID = '-1001883219679'
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    logger = logging.getLogger('django')

    allQuiz = Quiz.objects.all()
    for quiz in allQuiz:
        logger.info(f"Checking {quiz.quizTitle}")
        startTime = timezone.localtime(quiz.quizStartDate).time()
        now = datetime.datetime.now().time()
        logger.info(
            f"Check -> {quiz.quizTitle}: {startTime} and now {now} => {startTime.hour}{startTime.minute} ~ {now.hour}{now.minute}")
        if f"{startTime.hour}{startTime.minute}" == f"{now.hour}{now.minute}":
            message = f"КВИЗ '{quiz.quizTitle}' НАЧАЛСЯ:\n" \
                      f"Скорее заходи и участвуй!\n" \
                      f"Ссылка: http://zuvs.ru/quiz/{quiz.pk}"
            logger.info("NOW ^^^")
            try:
                bot.send_message(chat_id=chatID, text=message)
                logger.info("MESSAGE SENT ^^^")
            except BaseException as e:
                logger.info("ERROR")
                logger.info(e)
