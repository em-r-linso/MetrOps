from django.urls import include, path

from . import views

app_name = "core"
urlpatterns = [
    path("", views.HomepageView.as_view(), name="homepage"),
    path("accounts/", include("django.contrib.auth.urls")),
]
