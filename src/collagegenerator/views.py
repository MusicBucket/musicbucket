from django.http import HttpResponse
from django.views import generic

from api.modules.lastfm.client import LastfmClient
from collagegenerator.forms import CollageForm


class CollageFormView(generic.FormView):
    form_class = CollageForm
    template_name = "collagegenerator/collage.html"

    def form_valid(self, form: CollageForm) -> HttpResponse:
        image = LastfmClient.generate_collage(
            entity=form.cleaned_data["entity"],
            username=form.cleaned_data["username"],
            cols=form.cleaned_data["cols"],
            rows=form.cleaned_data["rows"],
            period=form.cleaned_data["period"]
        )
        response = HttpResponse(content_type="image/png")
        image.save(response, format="png")
        return response
