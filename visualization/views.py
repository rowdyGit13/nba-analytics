from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from .services.visualization_service import VisualizationService
import json

# Create your views here.

def visualization_page(request: HttpRequest) -> HttpResponse:
    """Renders the main visualization page with team and dataset selectors."""
    teams = VisualizationService.get_all_teams_for_select()
    datasets = VisualizationService.DATASET_OPTIONS
    context = {
        'teams': teams,
        'datasets': datasets.items(), # Pass items for easy looping in template
        'initial_chart_data': VisualizationService.get_chart_data(None, None) # Initial empty chart
    }
    return render(request, 'visualization/visualization_page.html', context)

def get_chart_data_htmx(request: HttpRequest) -> JsonResponse:
    """Handles HTMX request to fetch chart data based on selected team and dataset."""
    team_id = request.GET.get('team_id')
    dataset_key = request.GET.get('dataset_key')
    
    chart_data_json = VisualizationService.get_chart_data(team_id, dataset_key)
    chart_data = json.loads(chart_data_json)
    # Return data as JSON. The frontend (Alpine.js) will handle updating the chart.
    return JsonResponse(chart_data, safe=False)
