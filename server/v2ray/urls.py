from django.urls import path
from .views import V2rayAPIView, OperatorAPIView

urlpatterns = [
    path('', V2rayAPIView.as_view()),
    path('operator/', OperatorAPIView.as_view()),
]
