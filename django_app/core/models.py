from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = "student", "Student"
        TEACHER = "teacher", "Teacher"

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
    )

    def __str__(self):
        return f"{self.username} ({self.role})"



class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="projects",
        limit_choices_to={"role": User.Role.STUDENT},
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

from django.core.validators import MinValueValidator, MaxValueValidator


class Feedback(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="feedback_list",
    )
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="given_feedback",
        limit_choices_to={"role": User.Role.TEACHER},
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating}/5 by {self.teacher.username} on {self.project.title}"