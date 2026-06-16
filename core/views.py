import json
import math
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Avg
from .models import Location, Review, EmergencyRequest, Volunteer, ShelterVisit, SMSRequest, Notification

# ── Urgency Engine ──────────────────────────────────────────────────────────
URGENCY_KEYWORDS = {
    (9, 10): ['bleeding', 'unconscious', 'suicide', 'dying', 'attack', 'stabbed', 'overdose', 'not breathing', 'heart attack', 'stroke'],
    (7, 8):  ['3 days no food', 'child with me', 'collapsing', 'pregnant', 'baby', 'injured', 'fever', 'diabetic', 'medicine', 'days without'],
    (5, 6):  ['raining', 'no shelter tonight', 'cold', 'freezing', 'stranded', 'lost', 'night', 'outside', 'no food today'],
    (3, 4):  ['need food', 'looking for water', 'hungry', 'thirsty', 'shelter', 'help me find'],
    (1, 2):  ['where is', 'nearest', 'location', 'address', 'how to reach'],
}

NEED_KEYWORDS = {
    'Food': ['food', 'eat', 'hungry', 'meal', 'kitchen', 'bread'],
    'Shelter': ['shelter', 'sleep', 'stay', 'night', 'house', 'bed', 'roof'],
    'Water': ['water', 'drink', 'thirsty', 'dehydrated'],
    'Medical': ['medical', 'doctor', 'hospital', 'medicine', 'sick', 'injured', 'bleeding', 'fever'],
}

def score_urgency(text):
    text_lower = text.lower()
    score = 1
    label = 'Low'
    for (lo, hi), keywords in URGENCY_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                if hi > score:
                    score = hi
                    labels = {10: 'EMERGENCY', 9: 'EMERGENCY', 8: 'Critical', 7: 'Critical', 6: 'High', 5: 'High', 4: 'Medium', 3: 'Medium', 2: 'Low', 1: 'Low'}
                    label = labels.get(score, 'Low')
    needs = [need for need, kws in NEED_KEYWORDS.items() if any(k in text_lower for k in kws)]
    return score, label, needs

# ── Haversine ───────────────────────────────────────────────────────────────
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return round(2 * R * math.asin(math.sqrt(a)), 2)

# ── Pages ────────────────────────────────────────────────────────────────────
def home(request):
    stats = {
        'locations': Location.objects.filter(is_verified=True).count(),
        'volunteers': Volunteer.objects.filter(is_active=True).count(),
        'cities': Location.objects.values('city').distinct().count(),
        'emergencies': EmergencyRequest.objects.count(),
    }
    return render(request, 'core/home.html', {'stats': stats})

def user_map(request):
    locations = Location.objects.filter(is_verified=True)
    cities = Location.objects.values_list('city', flat=True).distinct()
    return render(request, 'core/user_map.html', {
        'locations': json.dumps([loc_to_dict(l) for l in locations]),
        'cities': list(cities),
    })

@login_required
def admin_map(request):
    locations = Location.objects.all()
    volunteers = Volunteer.objects.all()
    emergencies = EmergencyRequest.objects.order_by('-created_at')[:20]
    notifications = Notification.objects.filter(is_read=False)
    return render(request, 'core/admin_map.html', {
        'locations': json.dumps([loc_to_dict(l) for l in locations]),
        'volunteers': volunteers,
        'emergencies': emergencies,
        'notifications': notifications,
        'stats': {
            'total': locations.count(),
            'verified': locations.filter(is_verified=True).count(),
            'volunteers': Volunteer.objects.filter(is_active=True).count(),
            'emergencies': EmergencyRequest.objects.filter(is_resolved=False).count(),
        }
    })

def loc_to_dict(l):
    return {
        'id': l.id, 'name': l.name, 'category': l.category,
        'address': l.address, 'city': l.city, 'lat': l.lat, 'lng': l.lng,
        'phone': l.phone, 'hours': l.hours, 'seats_available': l.seats_available,
        'capacity': l.capacity, 'safety_level': l.safety_level,
        'is_verified': l.is_verified, 'description': l.description,
        'image': l.image.url if l.image else None,
    }

# ── API ──────────────────────────────────────────────────────────────────────
def api_locations(request):
    qs = Location.objects.filter(is_verified=True)
    category = request.GET.get('category')
    city = request.GET.get('city')
    q = request.GET.get('q')
    if category: qs = qs.filter(category=category)
    if city: qs = qs.filter(city__icontains=city)
    if q: qs = qs.filter(Q(name__icontains=q) | Q(address__icontains=q) | Q(description__icontains=q))
    return JsonResponse({'locations': [loc_to_dict(l) for l in qs]})

def api_nearby(request):
    try:
        lat = float(request.GET.get('lat'))
        lng = float(request.GET.get('lng'))
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Invalid coordinates'}, status=400)
    category = request.GET.get('category', '')
    qs = Location.objects.filter(is_verified=True)
    if category: qs = qs.filter(category=category)
    results = []
    for l in qs:
        d = haversine(lat, lng, l.lat, l.lng)
        item = loc_to_dict(l)
        item['distance'] = d
        results.append(item)
    results.sort(key=lambda x: x['distance'])
    return JsonResponse({'locations': results[:15]})

def api_directions(request):
    """Return OSRM route between two points"""
    try:
        user_lat = float(request.GET.get('user_lat'))
        user_lng = float(request.GET.get('user_lng'))
        dest_lat = float(request.GET.get('dest_lat'))
        dest_lng = float(request.GET.get('dest_lng'))
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Invalid coordinates'}, status=400)
    return JsonResponse({
        'user': {'lat': user_lat, 'lng': user_lng},
        'dest': {'lat': dest_lat, 'lng': dest_lng},
        'osrm_url': f'https://router.project-osrm.org/route/v1/driving/{user_lng},{user_lat};{dest_lng},{dest_lat}?overview=full&geometries=geojson'
    })

@csrf_exempt
def api_urgency(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    data = json.loads(request.body)
    message = data.get('message', '')
    contact = data.get('contact', '')
    score, label, needs = score_urgency(message)
    EmergencyRequest.objects.create(
        message=message, urgency_score=score, urgency_label=label,
        needs=', '.join(needs), contact=contact
    )
    return JsonResponse({
        'score': score, 'label': label, 'needs': needs,
        'call_emergency': score >= 8,
        'helplines': {'National Emergency': '112', 'Police': '100', 'Ambulance': '108', 'iCall': '9152987821'} if score >= 8 else {}
    })

@csrf_exempt
def api_volunteer_register(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    data = json.loads(request.body)
    v = Volunteer.objects.create(
        name=data['name'], phone=data['phone'], email=data.get('email', ''),
        skill=data['skill'], city=data['city'], available_days=data['available_days']
    )
    return JsonResponse({'id': v.id, 'message': 'Volunteer registered successfully!'})

def api_crowd_prediction(request, location_id):
    import datetime
    loc = get_object_or_404(Location, id=location_id)
    now = datetime.datetime.now()
    predictions = []
    for h in range(24):
        visits = ShelterVisit.objects.filter(location=loc, day_of_week=now.weekday(), hour=h)
        if visits.exists():
            occ = visits.aggregate(Avg('occupancy_percent'))['occupancy_percent__avg']
        else:
            if 0 <= h < 6: occ = 90
            elif 18 <= h < 22: occ = 75
            else: occ = 40
        predictions.append({'hour': h, 'occupancy': round(occ, 1)})
    best = sorted(predictions, key=lambda x: x['occupancy'])[:3]
    return JsonResponse({'location': loc.name, 'predictions': predictions, 'best_times': best})

@csrf_exempt
def api_sms(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    data = json.loads(request.body)
    phone = data.get('phone', 'unknown')
    message = data.get('message', '').strip().upper()
    parts = message.split()
    response = 'Invalid command. Use: FOOD DELHI or SHELTER MUMBAI'
    if len(parts) >= 2:
        cat_map = {'FOOD': 'food', 'SHELTER': 'shelter', 'WATER': 'water', 'MEDICAL': 'medical'}
        category = cat_map.get(parts[0])
        city = parts[1].title()
        if category:
            locs = Location.objects.filter(category=category, city__icontains=city, is_verified=True)[:3]
            if locs:
                response = f"{parts[0]} in {city}:\n" + "\n".join([f"- {l.name}: {l.address} Ph:{l.phone}" for l in locs])
            else:
                response = f"No {parts[0].lower()} found in {city}."
    SMSRequest.objects.create(phone_number=phone, message=message, response_sent=response)
    return JsonResponse({'response': response})

@csrf_exempt
def api_add_location(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    # Support both multipart (with image) and JSON
    if request.content_type and 'multipart' in request.content_type:
        data = request.POST
        image = request.FILES.get('image')
    else:
        data = json.loads(request.body)
        image = None
    loc = Location.objects.create(
        name=data['name'], category=data['category'], address=data['address'],
        city=data['city'], lat=float(data['lat']), lng=float(data['lng']),
        phone=data.get('phone', ''), hours=data.get('hours', '24/7'),
        seats_available=int(data.get('seats_available', 0)),
        capacity=int(data.get('capacity', 100)),
        description=data.get('description', ''), is_verified=False
    )
    if image:
        loc.image = image
        loc.save()
    return JsonResponse({'id': loc.id, 'message': 'Location added successfully!', 'image': loc.image.url if loc.image else None})

@csrf_exempt
def api_update_location(request, location_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    loc = get_object_or_404(Location, id=location_id)
    if request.content_type and 'multipart' in request.content_type:
        data = request.POST
        image = request.FILES.get('image')
        if image:
            loc.image = image
    else:
        data = json.loads(request.body)
    for field in ['name', 'address', 'phone', 'hours', 'seats_available', 'is_verified', 'description']:
        if field in data:
            setattr(loc, field, data[field])
    loc.save()
    return JsonResponse({'message': 'Updated!', 'image': loc.image.url if loc.image else None})

@csrf_exempt
def api_delete_location(request, location_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    loc = get_object_or_404(Location, id=location_id)
    loc.delete()
    return JsonResponse({'message': 'Deleted!'})

@csrf_exempt
def api_add_review(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    data = json.loads(request.body)
    loc = get_object_or_404(Location, id=data['location_id'])
    Review.objects.create(location=loc, reviewer_name=data['name'], rating=int(data['rating']), comment=data['comment'])
    return JsonResponse({'message': 'Review added!'})

def api_volunteers(request):
    skill = request.GET.get('skill')
    city = request.GET.get('city')
    qs = Volunteer.objects.filter(is_active=True)
    if skill: qs = qs.filter(skill=skill)
    if city: qs = qs.filter(city__icontains=city)
    return JsonResponse({'volunteers': [
        {'id': v.id, 'name': v.name, 'skill': v.get_skill_display(), 'city': v.city, 'phone': v.phone, 'available_days': v.available_days}
        for v in qs
    ]})

def api_stats(request):
    return JsonResponse({
        'total_locations': Location.objects.count(),
        'verified': Location.objects.filter(is_verified=True).count(),
        'by_category': {cat: Location.objects.filter(category=cat).count() for cat, _ in [('food','Food'),('shelter','Shelter'),('water','Water'),('medical','Medical')]},
        'volunteers': Volunteer.objects.filter(is_active=True).count(),
        'emergencies': EmergencyRequest.objects.count(),
        'sms_requests': SMSRequest.objects.count(),
    })
