from django.db import models

CATEGORY_CHOICES = [
    ('food', 'Food'),
    ('shelter', 'Shelter'),
    ('water', 'Water'),
    ('medical', 'Medical'),
    ('clothing', 'Clothing'),
]

CITY_CHOICES = [
    ('Delhi', 'Delhi'),
    ('Mumbai', 'Mumbai'),
    ('Bengaluru', 'Bengaluru'),
    ('Chennai', 'Chennai'),
    ('Kolkata', 'Kolkata'),
    ('Hyderabad', 'Hyderabad'),
    ('Pune', 'Pune'),
    ('Ahmedabad', 'Ahmedabad'),
]

class Location(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    address = models.TextField()
    city = models.CharField(max_length=50, choices=CITY_CHOICES)
    lat = models.FloatField()
    lng = models.FloatField()
    phone = models.CharField(max_length=20, blank=True)
    hours = models.CharField(max_length=100, default='24/7')
    seats_available = models.IntegerField(default=0)
    capacity = models.IntegerField(default=100)
    safety_level = models.IntegerField(default=3)  # 1-5
    is_verified = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='location_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.city})"

class Review(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='reviews')
    reviewer_name = models.CharField(max_length=100)
    rating = models.IntegerField(default=3)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.location.name}"

class EmergencyRequest(models.Model):
    message = models.TextField()
    urgency_score = models.IntegerField(default=1)
    urgency_label = models.CharField(max_length=50)
    needs = models.CharField(max_length=200)
    contact = models.CharField(max_length=100, blank=True)
    location_hint = models.CharField(max_length=200, blank=True)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Emergency #{self.id} - Score {self.urgency_score}"

SKILL_CHOICES = [
    ('food_delivery', 'Food Delivery'),
    ('shelter_assistance', 'Shelter Assistance'),
    ('medical_aid', 'Medical Aid'),
    ('counselling', 'Counselling'),
    ('transport', 'Transport'),
    ('clothing', 'Clothing Distribution'),
    ('general', 'General Help'),
]

class Volunteer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    skill = models.CharField(max_length=50, choices=SKILL_CHOICES)
    city = models.CharField(max_length=50, choices=CITY_CHOICES)
    available_days = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.skill} ({self.city})"

class ShelterVisit(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='visits')
    day_of_week = models.IntegerField()  # 0=Monday
    hour = models.IntegerField()
    occupancy_percent = models.FloatField()
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Visit at {self.location.name} day={self.day_of_week} hour={self.hour}"

class SMSRequest(models.Model):
    phone_number = models.CharField(max_length=20)
    message = models.TextField()
    response_sent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SMS from {self.phone_number}"

class Notification(models.Model):
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message[:50]
