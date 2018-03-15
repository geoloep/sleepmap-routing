from django.urls import path

from . import views

urlpatterns = [
    path('route/', views.Route.as_view()),
]