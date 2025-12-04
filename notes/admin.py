from django.contrib import admin

from .models import Board, Note


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "created_at", "updated_at")
    list_filter = ("user",)
    search_fields = ("name",)


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "board", "color", "tag", "last_edited")
    list_filter = ("color", "user", "board", "tag")
    search_fields = ("title", "content", "tag")

