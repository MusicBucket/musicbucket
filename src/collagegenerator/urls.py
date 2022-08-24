from django.urls import path

from collagegenerator import views

app_name = "collagegenerator"

urlpatterns = [
    path("", views.CollageFormView.as_view(), name="collage-generator"),
]
