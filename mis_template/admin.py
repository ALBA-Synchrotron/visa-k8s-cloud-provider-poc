# Register your models here.
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import *


class FeatureAdmin(SimpleHistoryAdmin):
    list_display = [field.name for field in Feature._meta.get_fields()]
    search_fields = ['id', 'code', 'description']
    list_filter = ('enabled',)


admin.site.register(Feature, FeatureAdmin)
