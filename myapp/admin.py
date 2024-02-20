from django.contrib import admin
from .models import WebLink

@admin.register(WebLink)
class WebLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'purpose', 'url')
    search_fields = ('title', 'description', 'tags')


