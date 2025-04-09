from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .services.search_service import SearchService # Import the service

def search_page(request: HttpRequest) -> HttpResponse:
    """Renders the main search page."""
    context = {
        'search_results': [],  # Initialize with empty results
        'max_cards': SearchService.MAX_RESULTS # Use constant from service
    }
    return render(request, 'search/search_page.html', context)

def perform_search(request: HttpRequest) -> HttpResponse:
    """Handles the search request using the SearchService and returns results via HTMX."""
    search_term = request.GET.get('search_term', '')
    search_type = request.GET.get('search_type', 'player')
    season = request.GET.get('season', '')

    results = []
    if search_term and season:
        results = SearchService.perform_search(search_term, search_type, season)
    else:
        # Handle cases where search term or season is missing, maybe return an error message
        pass 

    context = {'search_results': results} 
    
    # Always return the partial for HTMX requests or when form is submitted
    # The main page load is handled by search_page view
    return render(request, 'partials/_search_results.html', context)
