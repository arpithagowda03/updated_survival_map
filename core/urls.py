from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('map/', views.user_map, name='user_map'),
    path('admin-map/', views.admin_map, name='admin_map'),

    # API
    path('api/locations/', views.api_locations, name='api_locations'),
    path('api/nearby/', views.api_nearby, name='api_nearby'),
    path('api/directions/', views.api_directions, name='api_directions'),
    path('api/urgency/', views.api_urgency, name='api_urgency'),
    path('api/volunteer/register/', views.api_volunteer_register, name='api_volunteer_register'),
    path('api/volunteers/', views.api_volunteers, name='api_volunteers'),
    path('api/crowd/<int:location_id>/', views.api_crowd_prediction, name='api_crowd'),
    path('api/sms/', views.api_sms, name='api_sms'),
    path('api/location/add/', views.api_add_location, name='api_add_location'),
    path('api/location/<int:location_id>/update/', views.api_update_location, name='api_update_location'),
    path('api/location/<int:location_id>/delete/', views.api_delete_location, name='api_delete_location'),
    path('api/review/add/', views.api_add_review, name='api_add_review'),
    path('api/stats/', views.api_stats, name='api_stats'),
]
