from django.urls import path
from . import views

urlpatterns = [
    path('', views.visualization_page, name='visualization_page'),
    path('chart-data/', views.get_chart_data_htmx, name='get_chart_data_htmx'), # HTMX endpoint
] 