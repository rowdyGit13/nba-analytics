from django.shortcuts import render

# Create your views here.

def landing_page(request):
    """Renders the landing page."""
    return render(request, 'core/landing_page.html')
