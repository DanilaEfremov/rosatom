from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_list, name='chat_list'),
    path('<int:chat_id>/', login_required(views.chat_detail), name='chat_detail'),
]
