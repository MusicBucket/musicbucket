from django.urls import path

from front import views

app_name = 'front'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
]
