from django.db import models
from django.contrib.auth.models import User


class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=200)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    accuracy = models.IntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.test_name
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username
# Create your models here.
from django.utils import timezone


class WellbeingEntry(models.Model):
    MOOD_CHOICES = [
        ("great", "Great"),
        ("good", "Good"),
        ("okay", "Okay"),
        ("stressed", "Stressed"),
        ("tired", "Tired"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="wellbeing_entries"
    )
    date = models.DateField(default=timezone.localdate)
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
    stress_level = models.PositiveSmallIntegerField()
    sleep_hours = models.DecimalField(max_digits=4, decimal_places=1)
    study_hours = models.DecimalField(max_digits=4, decimal_places=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.mood}"

class SubjectResult(models.Model):
    SUBJECT_CHOICES = [
        ("Biology", "Biology"),
        ("Chemistry", "Chemistry"),
        ("Physics", "Physics"),
    ]

    test_result = models.ForeignKey(
        TestResult,
        on_delete=models.CASCADE,
        related_name="subject_results"
    )
    subject = models.CharField(
        max_length=20,
        choices=SUBJECT_CHOICES
    )
    score = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField(default=0)
    accuracy = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"{self.subject} - {self.accuracy}%"
