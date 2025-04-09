from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_page, name='search_page'),
    path('results/', views.perform_search, name='perform_search'), # Endpoint for HTMX search
] 