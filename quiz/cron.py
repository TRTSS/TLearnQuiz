from django.utils import timezone

from quiz.models import Quiz


def SendQuizScheldue():
    apiToken = '5854080741:AAG5eK_jf5130SKO3dd8EgihxfKdIVki0vE'
    chatID = '-1001883219679'
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    print ('hello crontab!')