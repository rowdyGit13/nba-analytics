from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    # Add other core app URLs here
] 