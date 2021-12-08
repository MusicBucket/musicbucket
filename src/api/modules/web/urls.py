from django.urls import path
from api.modules.web import views

urlpatterns = [
    path("stats/", views.StatsAPIView.as_view(), name="stats"),
]
