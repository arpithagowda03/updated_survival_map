from django.contrib import admin
from .models import Location, Review, EmergencyRequest, Volunteer, ShelterVisit, SMSRequest, Notification

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'city', 'is_verified', 'seats_available']
    list_filter = ['category', 'city', 'is_verified']
    search_fields = ['name', 'address']

@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ['name', 'skill', 'city', 'phone', 'is_active']
    list_filter = ['skill', 'city', 'is_active']

@admin.register(EmergencyRequest)
class EmergencyAdmin(admin.ModelAdmin):
    list_display = ['id', 'urgency_score', 'urgency_label', 'needs', 'is_resolved', 'created_at']
    list_filter = ['urgency_label', 'is_resolved']

admin.site.register(Review)
admin.site.register(ShelterVisit)
admin.site.register(SMSRequest)
admin.site.register(Notification)
