from django.contrib import admin

from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "color", "tags", "last_edited")
    list_filter = ("color", "user")
    search_fields = ("title", "content", "tags")

