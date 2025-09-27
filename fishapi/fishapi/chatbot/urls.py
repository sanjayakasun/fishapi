from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chat_view, name='chat'),
    path('api/chat/', views.chat_api, name='chat_api'),
    path('api/species/', views.species_list, name='species_list'),
    path('api/species/<int:species_id>/', views.species_detail, name='species_detail'),
]
