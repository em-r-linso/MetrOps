from django.views.generic import TemplateView, View, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render

from .models import Character, LifepathQuestion, LifepathAnswer, LifepathConfig


class Index(LoginRequiredMixin, TemplateView):
    template_name = "characters/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get just the characters owned by the current user
        context["characters"] = Character.objects.filter(owner=self.request.user)

        return context


class CharacterSheet(LoginRequiredMixin, DetailView):
    model = Character
    template_name = "characters/character_sheet.html"
    context_object_name = "character"


class Lifepath(LoginRequiredMixin, View):
    def get(self, request, question_id=None):
        """Request the lifepath page.

        If no question_id is provided, start at the first question.
        Otherwise, show the question with the provided ID."""

        if question_id is None:
            question = LifepathConfig.objects.first().first_question
            character = Character.objects.create(owner=request.user)
            request.session["character_id"] = character.pk
        else:
            question = LifepathQuestion.objects.get(pk=question_id)

        context = {"question": question}
        return render(request, "characters/lifepath.html", context)

    def post(self, request, question_id):
        """Submission of lifepath answers.

        If there is a followup question (or followup questin override), redirect to that question.
        Otherwise, redirect to the character sheet page."""

        selected_answer_id = request.POST.get("answer")
        selected_answer = LifepathAnswer.objects.get(pk=selected_answer_id)

        if selected_answer.followup_question_override:
            next_question = selected_answer.followup_question_override
        else:
            current_question = LifepathQuestion.objects.get(pk=question_id)
            next_question = current_question.followup_question

        if next_question:
            return redirect(
                "characters:lifepath_question", question_id=next_question.pk
            )
        else:
            character_id = request.session["character_id"]
            del request.session["character_id"]
            return redirect("characters:character_sheet", pk=character_id)
