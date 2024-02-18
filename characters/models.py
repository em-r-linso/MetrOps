from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class LifepathQuestion(models.Model):
    content = models.CharField(max_length=200)
    followup_question = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="previous_questions",
        # if no question is next, this is treated as the final question in the lifepath
        null=True,
        blank=True,
    )
    is_first_question = models.BooleanField(default=False)

    def __str__(self):
        return self.content


class LifepathAnswer(models.Model):
    content = models.CharField(max_length=200)
    question = models.ForeignKey(
        LifepathQuestion, on_delete=models.CASCADE, related_name="lifepath_answers"
    )
    followup_question_override = models.ForeignKey(
        LifepathQuestion,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.content


class LifepathConfig(models.Model):
    first_question = models.OneToOneField(
        LifepathQuestion,
        on_delete=models.SET_NULL,
        related_name="start_point",
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        if LifepathConfig.objects.exists() and not self.pk:
            # Prevents a new instance from being created if one already exists
            raise ValidationError("There can be only one LifepathConfig instance.")
        return super(LifepathConfig, self).save(*args, **kwargs)


class Character(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    owner = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="characters"
    )

    lifepath_answers = models.ManyToManyField(
        LifepathAnswer, through="CharacterLifepathAnswer", related_name="characters"
    )

    def __str__(self):
        return self.name


class CharacterLifepathAnswer(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    answer = models.ForeignKey(LifepathAnswer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.character.name} - {self.answer.content}"
