from django.contrib import admin
from .models import Quiz, QuizQuestion, QuizQuestionAnswer, QuizResult


# Register your models here.
admin.site.register(Quiz)
admin.site.register(QuizQuestion)
admin.site.register(QuizQuestionAnswer)
admin.site.register(QuizResult)