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

    def __str__(self):
        return f"[{self.id}] {self.quizTitle}"


class QuizResult(models.Model):
    quizRef = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    quizUser = models.ForeignKey(User, on_delete=models.CASCADE)

    scores = models.IntegerField()

    def __str__(self):
        return f'{self.quizUser} - {self.quizRef}'