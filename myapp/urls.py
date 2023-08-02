# project/app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('board/', views.post_list, name='board_list'),  # URL for listing board posts
    path('board/add/', views.post_create, name='board_create'),  # URL for creating board posts
    path('board/delete/<int:pk>/', views.post_delete, name='board_delete'),  # URL for deleting board posts
    path('board/update/<int:pk>/', views.PostEditView.as_view(), name='board_update'),  # URL for editing board posts
    path('board/<int:pk>/add/', views.comment_create, name='comment_create'),  # URL for creating board comments
    path('board/<int:pk>/delete/<int:comment_id>/', views.comment_delete, name='comment_delete'),  # URL for deleting board comments
]
