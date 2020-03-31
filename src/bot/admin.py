from django.contrib import admin

# Register your models here.
from bot import models as bot_models
from django.contrib import admin
from django.db.models.base import ModelBase

# Temporary, register manually
for name, var in bot_models.__dict__.items():
    if type(var) is ModelBase:
        admin.site.register(var)
