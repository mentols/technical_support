from django.urls import path
from communication.views import TicketsAPIView, TicketsAPIDetailView, \
    MessageAPIView


urlpatterns = [
    path('tickets/', TicketsAPIView.as_view()),
    path('tickets/<int:pk>/', TicketsAPIDetailView.as_view()),
    path('tickets/<int:pk>/messages/', MessageAPIView.as_view()),

]
