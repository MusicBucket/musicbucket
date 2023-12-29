import pylast
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from lastfmcollagegenerator import constants as lastfmconstants

from api.modules.lastfm.client import LastfmClient


class CollageForm(forms.Form):
    MAX_ROWS = 5
    MAX_COLUMNS = 5
    ENTITIES = (
        (lastfmconstants.ENTITY_ALBUM, _("Album")),
        (lastfmconstants.ENTITY_ARTIST, _("Artist")),
        (lastfmconstants.ENTITY_TRACK, _("Track")),
    )
    PERIODS = (
        (pylast.PERIOD_7DAYS, _("7 days")),
        (pylast.PERIOD_1MONTH, _("1 month")),
        (pylast.PERIOD_3MONTHS, _("3 months")),
        (pylast.PERIOD_6MONTHS, _("6 months")),
        (pylast.PERIOD_12MONTHS, _("12 months")),
        (pylast.PERIOD_OVERALL, _("overall")),
    )

    username = forms.CharField(
        label=_("Username"),
    )
    entity = forms.ChoiceField(
        label=_("Entity"),
        choices=ENTITIES,
    )
    rows = forms.IntegerField(
        label=_("Rows"),
        min_value=2,
        max_value=MAX_ROWS,

        widget=forms.TextInput,
    )
    cols = forms.IntegerField(
        label=_("Columns"),
        min_value=2,
        max_value=MAX_COLUMNS,
        widget=forms.TextInput,
    )
    period = forms.ChoiceField(
        label=_("Period"),
        choices=PERIODS
    )

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            LastfmClient().check_if_user_exists(username)
        except pylast.WSError as e:
            if e.details == "User not found":
                raise ValidationError(_("Username not found"))
        return username
