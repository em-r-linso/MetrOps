from django.views.generic import TemplateView
from django.shortcuts import render


class HomepageView(TemplateView):
    template_name = "core/homepage.html"


def homepage(request):
    return render(request, "core/homepage.html")
