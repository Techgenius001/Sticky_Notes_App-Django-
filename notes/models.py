from django.conf import settings
from django.db import models


class Note(models.Model):
    COLOR_CHOICES = [
        ("#C7A4FF", "Soft Purple"),
        ("#FFF176", "Electric Yellow"),
        ("#FF8A80", "Soft Coral"),
        ("#A5D6A7", "Mint"),
        ("#80CBC4", "Teal"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notes"
    )
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    x = models.IntegerField(default=50)
    y = models.IntegerField(default=50)
    width = models.IntegerField(default=220)
    height = models.IntegerField(default=220)
    color = models.CharField(max_length=7, choices=COLOR_CHOICES, default="#FFF176")
    tags = models.CharField(
        max_length=255, blank=True, help_text="Comma-separated tags (e.g. work,ideas)"
    )
    last_edited = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-last_edited"]

    def __str__(self) -> str:
        return self.title

