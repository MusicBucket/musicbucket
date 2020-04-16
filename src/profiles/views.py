from django.urls import reverse_lazy
from django.views.generic import RedirectView


class LoginView(RedirectView):
    permanent = False
    url = reverse_lazy('web:home')
