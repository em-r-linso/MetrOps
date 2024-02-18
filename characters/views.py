from typing import Any
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Character


class Index(LoginRequiredMixin, TemplateView):
    template_name = "characters/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get just the characters owned by the current user
        context["characters"] = Character.objects.filter(owner=self.request.user)

        return context
