from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('board/<int:board_id>/', views.dashboard, name='board_detail'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('boards/create/', views.create_board, name='create_board'),
    path('boards/<int:pk>/rename/', views.rename_board, name='rename_board'),
    path('boards/<int:pk>/delete/', views.delete_board, name='delete_board'),
    path('notes/create/', views.create_note, name='create_note'),
    path('notes/<int:pk>/update/', views.update_note, name='update_note'),
    path('notes/<int:pk>/delete/', views.delete_note, name='delete_note'),
    path('notes/<int:pk>/position/', views.update_note_position, name='update_note_position'),
    path('notes/<int:pk>/size/', views.update_note_size, name='update_note_size'),
    path('notes/<int:pk>/content/', views.update_note_content, name='update_note_content'),
]


