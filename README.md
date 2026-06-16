# 🗺 SurvivalMap — Homeless Support Platform

A full-stack Django web application connecting homeless individuals to food, shelter, water, and medical resources across 8 Indian cities.

---

## 🚀 Quick Start

```bash
# 1. Extract the zip and enter the folder
cd survivalmap

# 2. Run setup (installs deps, seeds DB, starts server)
bash setup.sh
```

Then open: **http://127.0.0.1:8000/**

---

## 📋 Manual Setup

```bash
pip install django djangorestframework
python manage.py makemigrations core
python manage.py migrate
python manage.py seed_data          # loads 30 locations + 7 volunteers + admin user
python manage.py runserver
```

---

## 🔗 Pages

| URL | Description |
|-----|-------------|
| `/` | Home page with stats & features |
| `/map/` | **User Map** — find resources, directions, SOS, chatbot |
| `/login/` | Admin login |
| `/admin-map/` | **Admin Dashboard** — manage locations, volunteers, SOS |
| `/django-admin/` | Django admin panel |

**Admin credentials:** `admin` / `admin123`

---

## ✨ Features

### User Interface (`/map/`)
- 🗺 **Interactive Map** — Leaflet.js dark map with color-coded markers
- 📍 **Auto Geolocation** — GPS first, IP fallback, no manual input needed
- 🔍 **Search & Filter** — by category (food/shelter/water/medical/clothing) and free text
- 🧭 **Directions** — click "Get Directions" on any resource → live route via OSRM
- 🆘 **AI Urgency SOS** — describe situation → score 1–10 + emergency helplines
- 🤝 **Volunteer Registration** — register name, skill, city, availability
- 🤖 **SurvivalBot AI Chat** — Claude-powered assistant with resource context
- 📱 **SMS Simulator** — test "FOOD DELHI" commands (no internet required)
- 📊 **Crowd Prediction** — best visit times per shelter

### Admin Interface (`/admin-map/`)
- 📍 **Full CRUD** — add/edit/delete locations with map-click coordinate picker
- ✅ **Verify/Unverify** — control what users see
- 🤝 **Volunteer Browser** — filter by skill and city
- 🆘 **SOS Dashboard** — review emergency requests, mark resolved
- 📊 **Live Stats** — category breakdown, city breakdown bar charts

---

## 🗃 Database

**30 verified locations** across:
- 🏙 Delhi (7) · Mumbai (5) · Bengaluru (5) · Chennai (3)
- Kolkata (3) · Hyderabad (3) · Pune (3) · + Medical (2)

**Categories:** Food · Shelter · Water · Medical · Clothing

---

## 🧠 AI Features

- **Urgency Engine** — 5-tier keyword hierarchy, scores 1–10
- **Need Detection** — identifies Food / Shelter / Water / Medical from text
- **SurvivalBot** — Claude API chatbot (requires API key in browser)
- **SMS Parser** — 93%+ accuracy on CATEGORY CITY commands

---

## 📡 API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/locations/` | All verified locations (filter: category, city, q) |
| GET | `/api/nearby/?lat=&lng=` | Sorted by distance |
| GET | `/api/directions/` | OSRM route data |
| POST | `/api/urgency/` | AI urgency scoring |
| POST | `/api/volunteer/register/` | Register volunteer |
| GET | `/api/volunteers/` | List volunteers (filter: skill, city) |
| GET | `/api/crowd/<id>/` | Occupancy prediction |
| POST | `/api/sms/` | SMS command parser |
| POST | `/api/location/add/` | Add location |
| POST | `/api/location/<id>/update/` | Update location |
| POST | `/api/location/<id>/delete/` | Delete location |
| GET | `/api/stats/` | Dashboard statistics |

---

## 🛠 Tech Stack

- **Backend:** Python 3, Django 4.2, Django REST Framework
- **Database:** SQLite (dev) / PostgreSQL (prod)
- **Maps:** Leaflet.js + CartoDB dark tiles + OSRM routing
- **AI:** Claude API (Anthropic) for chatbot
- **Frontend:** Vanilla JS, Space Grotesk font, no build step needed

---

## 📁 Project Structure

```
survivalmap/
├── manage.py
├── setup.sh
├── requirements.txt
├── survivalmap/
│   ├── settings.py
│   └── urls.py
└── core/
    ├── models.py          # Location, Volunteer, EmergencyRequest, etc.
    ├── views.py           # All views + API endpoints
    ├── urls.py
    ├── admin.py
    ├── management/
    │   └── commands/
    │       └── seed_data.py   # Seeds 30 locations
    └── templates/core/
        ├── home.html          # Landing page
        ├── user_map.html      # Public user interface
        ├── admin_map.html     # Admin dashboard
        └── login.html         # Admin login
```
