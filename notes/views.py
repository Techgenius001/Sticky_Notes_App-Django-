from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Note


def signup_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("dashboard")
    return render(request, "auth/signup.html", {"form": form})


def login_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect("dashboard")
    return render(request, "auth/login.html", {"form": form})


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("login")


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    notes = Note.objects.filter(user=request.user)
    return render(
        request,
        "notes/dashboard.html",
        {
            "notes": notes,
        },
    )


@login_required
@require_POST
def create_note(request: HttpRequest) -> HttpResponse:
    title = request.POST.get("title", "").strip() or "Untitled"
    color = request.POST.get("color") or "#FFF176"
    tags = request.POST.get("tags", "").strip()
    content = request.POST.get("content", "").strip()
    Note.objects.create(
        user=request.user,
        title=title,
        color=color,
        tags=tags,
        content=content,
    )
    messages.success(request, "Note created.")
    return redirect("dashboard")


@login_required
@require_POST
def update_note(request: HttpRequest, pk: int) -> HttpResponse:
    note = get_object_or_404(Note, pk=pk, user=request.user)
    note.title = request.POST.get("title", note.title)
    note.content = request.POST.get("content", note.content)
    note.color = request.POST.get("color", note.color)
    note.tags = request.POST.get("tags", note.tags)
    note.save()
    messages.success(request, "Note updated.")
    return redirect("dashboard")


@login_required
@require_POST
def delete_note(request: HttpRequest, pk: int) -> HttpResponse:
    note = get_object_or_404(Note, pk=pk, user=request.user)
    note.delete()
    messages.success(request, "Note deleted.")
    return redirect("dashboard")


@login_required
@require_POST
def update_note_position(request: HttpRequest, pk: int) -> JsonResponse:
    note = get_object_or_404(Note, pk=pk, user=request.user)
    try:
        x = int(request.POST.get("x"))
        y = int(request.POST.get("y"))
    except (TypeError, ValueError):
        return HttpResponseBadRequest("Invalid coordinates")
    note.x = x
    note.y = y
    note.save(update_fields=["x", "y", "last_edited"])
    return JsonResponse({"status": "ok"})


@login_required
@require_POST
def update_note_size(request: HttpRequest, pk: int) -> JsonResponse:
    note = get_object_or_404(Note, pk=pk, user=request.user)
    try:
        width = int(request.POST.get("width"))
        height = int(request.POST.get("height"))
    except (TypeError, ValueError):
        return HttpResponseBadRequest("Invalid size")
    note.width = max(160, width)
    note.height = max(160, height)
    note.save(update_fields=["width", "height", "last_edited"])
    return JsonResponse({"status": "ok"})

