from django.views import generic


class MusicView(generic.TemplateView):
    template_name = 'app/music.html'
