from django.urls import path
from .views import ItemAPIView

urlpatterns = [
    path('items/', ItemAPIView.as_view(), name='item-api'),
]
