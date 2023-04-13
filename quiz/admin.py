from django.contrib import admin
from .models import Quiz, QuizQuestion, QuizQuestionAnswer, QuizResult, Invite, XPBonus

# Register your models here.
admin.site.register(Quiz)
admin.site.register(QuizQuestionAnswer)


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'quizUser', 'quizRef', 'scores']
    list_display_links = ['id']
    search_fields = ['quizUser', 'quizRef']
    list_filter = ['quizRef']


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'questionText']


@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    list_display = ['id', 'inviter', 'taker', 'date']


@admin.register(XPBonus)
class XPBonusAdmin(admin.ModelAdmin):
    list_display = ['id', 'recipient', 'xpAmount']
