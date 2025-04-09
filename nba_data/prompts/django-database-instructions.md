# Django Database Instructions

Follow these instructions to create a new model in the database.

## Guidelines

- User IDs should be handled using Django's built-in User model or a custom user model with proper authentication.
- For third-party auth like Clerk, store the external ID as a CharField with a unique constraint.

## Step 1: Create the Model

This is an example of how to create a new model in the database.

This file should be in your app's `models.py` file.

```python
from django.db import models
from django.utils import timezone

class MembershipChoices(models.TextChoices):
    FREE = "free", "Free"
    PRO = "pro", "Pro"

class Profile(models.Model):
    user_id = models.CharField(max_length=255, primary_key=True)
    membership = models.CharField(
        max_length=10,
        choices=MembershipChoices.choices,
        default=MembershipChoices.FREE
    )
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile: {self.user_id}"
    
    class Meta:
        db_table = "profiles"
```

After creating the model, register it in the app's `admin.py`:

```python
from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'membership', 'created_at', 'updated_at')
    search_fields = ('user_id', 'stripe_customer_id')
    list_filter = ('membership',)
```

## Step 2: Create the Database Queries

This is an example of how to create queries for the model.

This file should be named `profiles_repository.py` and placed in a `repositories` folder within your app.

```python
from typing import Optional, List, Dict, Any
from .models import Profile

class ProfileRepository:
    @staticmethod
    def create_profile(data: Dict[str, Any]) -> Profile:
        try:
            profile = Profile.objects.create(**data)
            return profile
        except Exception as e:
            print(f"Error creating profile: {e}")
            raise Exception("Failed to create profile")

    @staticmethod
    def get_profile_by_user_id(user_id: str) -> Optional[Profile]:
        try:
            return Profile.objects.filter(user_id=user_id).first()
        except Exception as e:
            print(f"Error getting profile by user ID: {e}")
            raise Exception("Failed to get profile")

    @staticmethod
    def get_all_profiles() -> List[Profile]:
        return Profile.objects.all()

    @staticmethod
    def update_profile(user_id: str, data: Dict[str, Any]) -> Optional[Profile]:
        try:
            profile = Profile.objects.filter(user_id=user_id).first()
            if profile:
                for key, value in data.items():
                    setattr(profile, key, value)
                profile.save()
                return profile
            return None
        except Exception as e:
            print(f"Error updating profile: {e}")
            raise Exception("Failed to update profile")

    @staticmethod
    def update_profile_by_stripe_customer_id(stripe_customer_id: str, data: Dict[str, Any]) -> Optional[Profile]:
        try:
            profile = Profile.objects.filter(stripe_customer_id=stripe_customer_id).first()
            if profile:
                for key, value in data.items():
                    setattr(profile, key, value)
                profile.save()
                return profile
            return None
        except Exception as e:
            print(f"Error updating profile by stripe customer ID: {e}")
            raise Exception("Failed to update profile")

    @staticmethod
    def delete_profile(user_id: str) -> bool:
        try:
            profile = Profile.objects.filter(user_id=user_id).first()
            if profile:
                profile.delete()
                return True
            return False
        except Exception as e:
            print(f"Error deleting profile: {e}")
            raise Exception("Failed to delete profile")
```

## Step 3: Create the Service Layer

This is an example of how to create a service layer for business logic.

This file should be named `profiles_service.py` and placed in a `services` folder within your app.

```python
from typing import Dict, Any, List, Optional
from .repositories.profiles_repository import ProfileRepository
from .models import Profile

class ProfileService:
    @staticmethod
    def create_profile(data: Dict[str, Any]) -> Profile:
        return ProfileRepository.create_profile(data)

    @staticmethod
    def get_profile_by_user_id(user_id: str) -> Optional[Profile]:
        return ProfileRepository.get_profile_by_user_id(user_id)

    @staticmethod
    def get_all_profiles() -> List[Profile]:
        return ProfileRepository.get_all_profiles()

    @staticmethod
    def update_profile(user_id: str, data: Dict[str, Any]) -> Optional[Profile]:
        return ProfileRepository.update_profile(user_id, data)

    @staticmethod
    def update_profile_by_stripe_customer_id(stripe_customer_id: str, data: Dict[str, Any]) -> Optional[Profile]:
        return ProfileRepository.update_profile_by_stripe_customer_id(stripe_customer_id, data)

    @staticmethod
    def delete_profile(user_id: str) -> bool:
        return ProfileRepository.delete_profile(user_id)
```

## Step 4: Create the Views/Controllers

This is an example of how to create API views for the model.

This file should be named `profiles_views.py` and placed in your app.

```python
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from .services.profiles_service import ProfileService
from django.shortcuts import render

# Function-based views for API endpoints
@csrf_exempt
@require_http_methods(["POST"])
def create_profile(request):
    try:
        data = json.loads(request.body)
        profile = ProfileService.create_profile(data)
        return JsonResponse({
            "status": "success", 
            "message": "Profile created successfully", 
            "data": {
                "user_id": profile.user_id,
                "membership": profile.membership,
                "stripe_customer_id": profile.stripe_customer_id,
                "stripe_subscription_id": profile.stripe_subscription_id,
                "created_at": profile.created_at.isoformat(),
                "updated_at": profile.updated_at.isoformat()
            }
        })
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

@require_http_methods(["GET"])
def get_profile(request, user_id):
    try:
        profile = ProfileService.get_profile_by_user_id(user_id)
        if not profile:
            return JsonResponse({"status": "error", "message": "Profile not found"}, status=404)
        
        return JsonResponse({
            "status": "success", 
            "message": "Profile retrieved successfully", 
            "data": {
                "user_id": profile.user_id,
                "membership": profile.membership,
                "stripe_customer_id": profile.stripe_customer_id,
                "stripe_subscription_id": profile.stripe_subscription_id,
                "created_at": profile.created_at.isoformat(),
                "updated_at": profile.updated_at.isoformat()
            }
        })
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

@require_http_methods(["GET"])
def get_all_profiles(request):
    try:
        profiles = ProfileService.get_all_profiles()
        profiles_data = [{
            "user_id": profile.user_id,
            "membership": profile.membership,
            "stripe_customer_id": profile.stripe_customer_id,
            "stripe_subscription_id": profile.stripe_subscription_id,
            "created_at": profile.created_at.isoformat(),
            "updated_at": profile.updated_at.isoformat()
        } for profile in profiles]
        
        return JsonResponse({
            "status": "success", 
            "message": "Profiles retrieved successfully", 
            "data": profiles_data
        })
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

@csrf_exempt
@require_http_methods(["PUT"])
def update_profile(request, user_id):
    try:
        data = json.loads(request.body)
        profile = ProfileService.update_profile(user_id, data)
        if not profile:
            return JsonResponse({"status": "error", "message": "Profile not found"}, status=404)
        
        return JsonResponse({
            "status": "success", 
            "message": "Profile updated successfully", 
            "data": {
                "user_id": profile.user_id,
                "membership": profile.membership,
                "stripe_customer_id": profile.stripe_customer_id,
                "stripe_subscription_id": profile.stripe_subscription_id,
                "created_at": profile.created_at.isoformat(),
                "updated_at": profile.updated_at.isoformat()
            }
        })
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_profile(request, user_id):
    try:
        success = ProfileService.delete_profile(user_id)
        if not success:
            return JsonResponse({"status": "error", "message": "Profile not found"}, status=404)
        
        return JsonResponse({
            "status": "success", 
            "message": "Profile deleted successfully"
        })
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

# HTMX view for profile display
def profile_detail_htmx(request, user_id):
    profile = ProfileService.get_profile_by_user_id(user_id)
    
    # Check if it's an HTMX request
    if request.headers.get('HX-Request'):
        # For HTMX requests, return just the profile fragment
        return render(request, 'partials/_profile_detail.html', {'profile': profile})
    else:
        # For regular requests, return the full page
        return render(request, 'profile_detail.html', {'profile': profile})
```

## Step 5: Configure URLs

Create or update the `urls.py` file in your app:

```python
from django.urls import path
from . import profiles_views

urlpatterns = [
    path('api/profiles/', profiles_views.create_profile, name='create_profile'),
    path('api/profiles/all/', profiles_views.get_all_profiles, name='get_all_profiles'),
    path('api/profiles/<str:user_id>/', profiles_views.get_profile, name='get_profile'),
    path('api/profiles/<str:user_id>/update/', profiles_views.update_profile, name='update_profile'),
    path('api/profiles/<str:user_id>/delete/', profiles_views.delete_profile, name='delete_profile'),
    
    # HTMX URL
    path('profiles/<str:user_id>/', profiles_views.profile_detail_htmx, name='profile_detail'),
]
```

## Step 6: Create Migrations and Apply Them

```bash
python manage.py makemigrations
python manage.py migrate
```

## Step 7: Create Templates for HTMX (Optional)

Create a base template `templates/base.html`:

```html
{% load static %}
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Django App{% endblock %}</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Alpine.js -->
    <script src="https://cdn.alpinejs.org/dist/cdn.min.js" defer></script>
    <!-- HTMX -->
    <script src="https://unpkg.com/htmx.org@1.9.6"></script>
    {% block extra_head %}{% endblock %}
</head>
<body class="bg-gray-100">
    <div class="container mx-auto p-4">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```

Create a profile detail template `templates/profile_detail.html`:

```html
{% extends "base.html" %}

{% block title %}Profile Details{% endblock %}

{% block content %}
    <div class="max-w-2xl mx-auto">
        <h1 class="text-2xl font-bold mb-6">Profile Details</h1>
        
        <div id="profile-container">
            {% include "partials/_profile_detail.html" with profile=profile %}
        </div>
        
        <div class="mt-6" x-data="{ showEditForm: false }">
            <button 
                @click="showEditForm = !showEditForm" 
                class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded">
                Edit Profile
            </button>
            
            <div x-show="showEditForm" class="mt-4 p-4 bg-white rounded shadow">
                <h2 class="text-xl font-semibold mb-4">Edit Profile</h2>
                <form hx-put="{% url 'update_profile' profile.user_id %}" 
                      hx-target="#profile-container" 
                      hx-swap="innerHTML"
                      @submit="showEditForm = false">
                    
                    <div class="mb-4">
                        <label class="block text-gray-700 mb-2">Membership</label>
                        <select name="membership" class="w-full p-2 border rounded">
                            <option value="free" {% if profile.membership == 'free' %}selected{% endif %}>Free</option>
                            <option value="pro" {% if profile.membership == 'pro' %}selected{% endif %}>Pro</option>
                        </select>
                    </div>
                    
                    <div class="mb-4">
                        <label class="block text-gray-700 mb-2">Stripe Customer ID</label>
                        <input type="text" name="stripe_customer_id" 
                               value="{{ profile.stripe_customer_id }}" 
                               class="w-full p-2 border rounded">
                    </div>
                    
                    <div class="mb-4">
                        <label class="block text-gray-700 mb-2">Stripe Subscription ID</label>
                        <input type="text" name="stripe_subscription_id" 
                               value="{{ profile.stripe_subscription_id }}" 
                               class="w-full p-2 border rounded">
                    </div>
                    
                    <button type="submit" 
                            class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded">
                        Save Changes
                    </button>
                </form>
            </div>
        </div>
    </div>
{% endblock %}
```

Create a partial template `templates/partials/_profile_detail.html`:

```html
<div class="bg-white p-6 rounded-lg shadow-md">
    <div class="mb-4 pb-4 border-b">
        <h2 class="text-xl font-semibold">User ID</h2>
        <p class="text-gray-700">{{ profile.user_id }}</p>
    </div>
    
    <div class="mb-4 pb-4 border-b">
        <h2 class="text-xl font-semibold">Membership</h2>
        <p class="text-gray-700">
            {% if profile.membership == 'pro' %}
                <span class="bg-purple-100 text-purple-800 px-2 py-1 rounded">Pro</span>
            {% else %}
                <span class="bg-gray-100 text-gray-800 px-2 py-1 rounded">Free</span>
            {% endif %}
        </p>
    </div>
    
    <div class="mb-4 pb-4 border-b">
        <h2 class="text-xl font-semibold">Stripe Customer ID</h2>
        <p class="text-gray-700">{{ profile.stripe_customer_id|default:"Not set" }}</p>
    </div>
    
    <div class="mb-4 pb-4 border-b">
        <h2 class="text-xl font-semibold">Stripe Subscription ID</h2>
        <p class="text-gray-700">{{ profile.stripe_subscription_id }}</p>
    </div>
    
    <div class="mb-4 pb-4 border-b">
        <h2 class="text-xl font-semibold">Created At</h2>
        <p class="text-gray-700">{{ profile.created_at|date:"F j, Y H:i" }}</p>
    </div>
    
    <div>
        <h2 class="text-xl font-semibold">Last Updated</h2>
        <p class="text-gray-700">{{ profile.updated_at|date:"F j, Y H:i" }}</p>
    </div>
</div>
```
