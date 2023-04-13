from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


# Create your models here
class QuizQuestionAnswer(models.Model):
    answerText = models.CharField(max_length=255)

    def __str__(self):
        return self.answerText


class QuizQuestion(models.Model):
    questionText = models.TextField()
    questionAnswers = models.ManyToManyField(QuizQuestionAnswer)
    questionRightAnswerId = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.questionText}'


class Quiz(models.Model):
    quizTitle = models.CharField(max_length=255)
    quizStartDate = models.DateTimeField(auto_now=False, auto_now_add=False, null=False, default=timezone.now)
    quizEndDate = models.DateTimeField(auto_now=False, auto_now_add=False, null=False, default=timezone.now)
    quizQuestions = models.ManyToManyField(QuizQuestion)
    quizSponsorTitle = models.CharField(max_length=100, null=True, blank=True)
    quizSponsorImage = models.ImageField(null=True, blank=True, upload_to="sponsorImage/")

    def __str__(self):
        return f"[{self.id}] {self.quizTitle}"


class QuizResult(models.Model):
    quizRef = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name='Квиз')
    quizUser = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Участник')

    scores = models.IntegerField(verbose_name='Счёт')

    class Meta:
        verbose_name = 'Результат квиза'
        verbose_name_plural = 'Результаты квизов'

    def __str__(self):
        return f'{self.quizUser} - {self.quizRef}'