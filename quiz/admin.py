from django.contrib import admin
from .models import Quiz, QuizQuestion, QuizQuestionAnswer, QuizResult

# Register your models here.
admin.site.register(Quiz)
admin.site.register(QuizQuestion)
admin.site.register(QuizQuestionAnswer)


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'quizUser', 'quizRef', 'scores']
    list_display_links = ['id']
    search_fields = ['quizUser', 'quizRef']
    list_filter = ['quizRef']
