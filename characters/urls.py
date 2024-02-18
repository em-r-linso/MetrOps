from django.urls import path

from . import views

app_name = "characters"
urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("lifepath/", views.Lifepath.as_view(), name="lifepath_start"),
    path(
        "lifepath/<int:question_id>/",
        views.Lifepath.as_view(),
        name="lifepath_question",
    ),
    path(
        "character/<int:pk>/",
        views.CharacterSheet.as_view(),
        name="character_sheet",
    ),
]
