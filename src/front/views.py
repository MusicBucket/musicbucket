from django.views import generic


class HomeView(generic.TemplateView):
    template_name = 'front/home.html'

    def dispatch(self, request, *args, **kwargs):
        # TODO: Redirect if the user is logged in
        return super().dispatch(request, *args, **kwargs)
