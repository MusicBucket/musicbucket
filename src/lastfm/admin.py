from django.contrib import admin

from lastfm.models import LastfmUser


class LastfmUserInline(admin.StackedInline):
    model = LastfmUser


@admin.register(LastfmUser)
class LastfmUserAdmin(admin.ModelAdmin):
    pass
