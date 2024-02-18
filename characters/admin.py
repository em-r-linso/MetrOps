from django.contrib import admin
from .models import Character, LifepathQuestion, LifepathAnswer, LifepathConfig


class LifepathAnswerInline(admin.TabularInline):
    model = LifepathAnswer
    extra = 3
    fk_name = "question"
    fields = ["content", "followup_question_override"]


class LifepathQuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Content", {"fields": ["content"]}),
        ("Followup Question", {"fields": ["followup_question"]}),
    ]
    inlines = [LifepathAnswerInline]


class CharacterLifepathAnswerInline(admin.TabularInline):
    model = Character.lifepath_answers.through
    extra = 3


class CharacterAdmin(admin.ModelAdmin):
    inlines = [CharacterLifepathAnswerInline]


admin.site.register(Character, CharacterAdmin)
admin.site.register(LifepathQuestion, LifepathQuestionAdmin)
admin.site.register(LifepathConfig)
