from django.urls import path
from .views import predict_image
from .views import explore_more_Grad_CAM

urlpatterns = [
    path('predict/', predict_image),
    path('explore_more_grad_cam/', explore_more_Grad_CAM),
]
