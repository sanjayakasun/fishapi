from django.urls import path
from .views import predict_image
from .views import explore_more_Grad_CAM
from . import views

urlpatterns = [
    path('predict/', predict_image),
    path('explore_more_grad_cam/', explore_more_Grad_CAM),
    path("fish/<str:species_id>/", views.get_fish_details, name="get_fish_details"),
]
