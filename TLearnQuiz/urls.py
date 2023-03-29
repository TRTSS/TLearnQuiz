"""TLearnQuiz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from quiz.views import play_quiz, register_request, login_request, check_access_to_quiz, send_quiz_result, \
    get_quiz_leaders, bot_connection, get_index, get_effects_sandbox

urlpatterns = [
    path('admin/', admin.site.urls),
    path('quiz/<int:quizId>', play_quiz, name='quiz'),
    path('regist/', register_request, name='regist'),
    path('login/', login_request, name='login'),
    path('connect', bot_connection, name='botConnection'),
    path('sandbox', get_effects_sandbox, name='sandbox'),
    path('', get_index, name='index'),
    path('api/check_access_to_quiz', check_access_to_quiz, name='apiCheckAccessToQuiz'),
    path('api/send_quiz_result', send_quiz_result, name='apiSendQuizResult'),
    path('api/get_quiz_leaders', get_quiz_leaders, name='apiGetQuizLeaders'),
]
