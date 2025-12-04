from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Board, Note


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
def dashboard(request: HttpRequest, board_id: int = None) -> HttpResponse:
    boards = Board.objects.filter(user=request.user)
    
    # Create default board if user has none
    if not boards.exists():
        board = Board.objects.create(user=request.user, name="My Board")
    else:
        # Get selected board or first board
        if board_id:
            board = get_object_or_404(Board, pk=board_id, user=request.user)
        else:
            board = boards.first()
    
    # Order by created_at ascending so newer notes render last (on top)
    notes = Note.objects.filter(user=request.user, board=board).order_by('created_at')
    return render(
        request,
        "notes/dashboard.html",
        {
            "notes": notes,
            "boards": boards,
            "current_board": board,
        },
    )


@login_required
@require_POST
def create_note(request: HttpRequest) -> HttpResponse:
    import random
    
    board_id = request.POST.get("board_id")
    board = get_object_or_404(Board, pk=board_id, user=request.user)
    
    title = request.POST.get("title", "").strip() or "Untitled"
    color = request.POST.get("color") or "#FFF176"
    tag = request.POST.get("tag", "").strip()
    content = request.POST.get("content", "").strip()
    
    # Randomize initial position to avoid overlapping
    x = random.randint(50, 400)
    y = random.randint(50, 300)
    
    Note.objects.create(
        user=request.user,
        board=board,
        title=title,
        color=color,
        tag=tag,
        content=content,
        x=x,
        y=y,
    )
    messages.success(request, "Note created.")
    return redirect("board_detail", board_id=board.id)


@login_required
@require_POST
def update_note(request: HttpRequest, pk: int) -> HttpResponse:
    note = get_object_or_404(Note, pk=pk, user=request.user)
    note.title = request.POST.get("title", note.title)
    note.content = request.POST.get("content", note.content)
    note.color = request.POST.get("color", note.color)
    note.tag = request.POST.get("tag", note.tag)
    note.save()
    messages.success(request, "Note updated.")
    return redirect("board_detail", board_id=note.board.id)


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


@login_required
@require_POST
def update_note_content(request: HttpRequest, pk: int) -> JsonResponse:
    note = get_object_or_404(Note, pk=pk, user=request.user)
    content = request.POST.get("content", "")
    note.content = content
    note.save(update_fields=["content", "last_edited"])
    return JsonResponse({"status": "ok"})


@login_required
@require_POST
def create_board(request: HttpRequest) -> HttpResponse:
    name = request.POST.get("name", "").strip() or "New Board"
    board = Board.objects.create(user=request.user, name=name)
    messages.success(request, f"Board '{name}' created.")
    return redirect("board_detail", board_id=board.id)


@login_required
@require_POST
def rename_board(request: HttpRequest, pk: int) -> HttpResponse:
    board = get_object_or_404(Board, pk=pk, user=request.user)
    name = request.POST.get("name", "").strip() or board.name
    board.name = name
    board.save()
    messages.success(request, f"Board renamed to '{name}'.")
    return redirect("board_detail", board_id=board.id)


@login_required
@require_POST
def delete_board(request: HttpRequest, pk: int) -> HttpResponse:
    board = get_object_or_404(Board, pk=pk, user=request.user)
    board_name = board.name
    board.delete()
    messages.success(request, f"Board '{board_name}' deleted.")
    return redirect("dashboard")

