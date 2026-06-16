from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Location, Volunteer, ShelterVisit

LOCATIONS = [
    # DELHI - Food (5)
    {"name": "Akshaya Patra Delhi", "category": "food", "address": "12 Vasant Kunj, New Delhi", "city": "Delhi", "lat": 28.5355, "lng": 77.1568, "phone": "011-26132400", "hours": "7AM-9PM", "seats_available": 80, "capacity": 200, "safety_level": 5, "description": "Free hot meals for 5000+ daily. Vegetarian food provided."},
    {"name": "Gurdwara Bangla Sahib Langar", "category": "food", "address": "Connaught Place, New Delhi", "city": "Delhi", "lat": 28.6270, "lng": 77.2090, "phone": "011-23364812", "hours": "24/7", "seats_available": 150, "capacity": 500, "safety_level": 5, "description": "Free community langar (meals) for all 24x7."},
    {"name": "Robin Hood Army Delhi", "category": "food", "address": "Lajpat Nagar, New Delhi", "city": "Delhi", "lat": 28.5667, "lng": 77.2433, "phone": "9810000001", "hours": "6PM-9PM", "seats_available": 60, "capacity": 150, "safety_level": 4, "description": "Weekly food distribution drives across Delhi."},
    # DELHI - Shelter (3)
    {"name": "DUSIB Night Shelter Kashmere Gate", "category": "shelter", "address": "Near Kashmere Gate Metro, Delhi", "city": "Delhi", "lat": 28.6669, "lng": 77.2283, "phone": "011-23930131", "hours": "8PM-8AM", "seats_available": 45, "capacity": 120, "safety_level": 4, "description": "Delhi Urban Shelter Improvement Board night shelter."},
    {"name": "Aashray Adhikar Abhiyan Shelter", "category": "shelter", "address": "Yamuna Pushta, Old Delhi", "city": "Delhi", "lat": 28.6562, "lng": 77.2410, "phone": "9811070670", "hours": "24/7", "seats_available": 30, "capacity": 80, "safety_level": 3, "description": "NGO-run shelter for homeless families."},
    # DELHI - Water (2)
    {"name": "Delhi Jal Board Water ATM Rohini", "category": "water", "address": "Sector 13, Rohini, Delhi", "city": "Delhi", "lat": 28.7041, "lng": 77.1025, "phone": "1800-180-0688", "hours": "24/7", "seats_available": 0, "capacity": 0, "safety_level": 5, "description": "24x7 potable water dispensing unit."},
    {"name": "Water Kiosk Connaught Place", "category": "water", "address": "Block K, Connaught Place, Delhi", "city": "Delhi", "lat": 28.6315, "lng": 77.2167, "phone": "", "hours": "6AM-10PM", "seats_available": 0, "capacity": 0, "safety_level": 5, "description": "Municipal water kiosk with clean drinking water."},
    # MUMBAI - Food (3)
    {"name": "Roti Bank Mumbai", "category": "food", "address": "Dharavi, Mumbai", "city": "Mumbai", "lat": 19.0440, "lng": 72.8521, "phone": "9820000001", "hours": "12PM-3PM", "seats_available": 100, "capacity": 300, "safety_level": 4, "description": "Free meal distribution for homeless and daily wage workers."},
    {"name": "Feeding India Mumbai Hub", "category": "food", "address": "Kurla West, Mumbai", "city": "Mumbai", "lat": 19.0728, "lng": 72.8826, "phone": "9320000002", "hours": "7AM-7PM", "seats_available": 70, "capacity": 200, "safety_level": 4, "description": "Zomato-backed food redistribution network."},
    {"name": "Dargah Haji Ali Langar", "category": "food", "address": "Haji Ali Dargah, Worli, Mumbai", "city": "Mumbai", "lat": 18.9827, "lng": 72.8090, "phone": "022-23528041", "hours": "5:30AM-10PM", "seats_available": 200, "capacity": 500, "safety_level": 5, "description": "Free community meals at historic dargah."},
    # MUMBAI - Shelter (2)
    {"name": "MCGM Night Shelter Dharavi", "category": "shelter", "address": "Dharavi Main Road, Mumbai", "city": "Mumbai", "lat": 19.0372, "lng": 72.8548, "phone": "022-24129700", "hours": "8PM-7AM", "seats_available": 40, "capacity": 100, "safety_level": 3, "description": "Municipal corporation night shelter."},
    {"name": "Snehasadan Women Shelter", "category": "shelter", "address": "Bandra West, Mumbai", "city": "Mumbai", "lat": 19.0596, "lng": 72.8295, "phone": "022-26403636", "hours": "24/7", "seats_available": 20, "capacity": 50, "safety_level": 5, "description": "Safe shelter exclusively for women and children."},
    # BENGALURU - Food (2)
    {"name": "Akshaya Patra Bengaluru", "category": "food", "address": "Rajajinagar Industrial Area, Bengaluru", "city": "Bengaluru", "lat": 12.9853, "lng": 77.5530, "phone": "080-23286346", "hours": "7AM-2PM", "seats_available": 100, "capacity": 300, "safety_level": 5, "description": "Largest mid-day meal kitchen in India."},
    {"name": "ISKCON Food for Life Bengaluru", "category": "food", "address": "Hare Krishna Hill, Rajajinagar, Bengaluru", "city": "Bengaluru", "lat": 12.9857, "lng": 77.5523, "phone": "080-23471956", "hours": "11AM-3PM", "seats_available": 60, "capacity": 200, "safety_level": 5, "description": "Free prasadam meals for all."},
    # BENGALURU - Shelter (2)
    {"name": "Asha Kiran Shelter Bengaluru", "category": "shelter", "address": "Shivajinagar, Bengaluru", "city": "Bengaluru", "lat": 12.9812, "lng": 77.5984, "phone": "080-22864400", "hours": "6PM-8AM", "seats_available": 35, "capacity": 90, "safety_level": 4, "description": "BBMP-run night shelter with meals."},
    {"name": "Sanidhya Trust Shelter", "category": "shelter", "address": "Koramangala 4th Block, Bengaluru", "city": "Bengaluru", "lat": 12.9352, "lng": 77.6245, "phone": "9741234567", "hours": "24/7", "seats_available": 15, "capacity": 40, "safety_level": 4, "description": "NGO shelter for homeless youth."},
    # BENGALURU - Water (1)
    {"name": "BBMP Water ATM Majestic", "category": "water", "address": "Kempegowda Bus Stand Area, Bengaluru", "city": "Bengaluru", "lat": 12.9774, "lng": 77.5713, "phone": "1916", "hours": "24/7", "seats_available": 0, "capacity": 0, "safety_level": 5, "description": "24hr potable water dispensing unit near bus stand."},
    # CHENNAI - Food (2)
    {"name": "Amma Unavagam Chennai", "category": "food", "address": "Anna Salai, Chennai", "city": "Chennai", "lat": 13.0827, "lng": 80.2707, "phone": "044-25384800", "hours": "7AM-11PM", "seats_available": 120, "capacity": 400, "safety_level": 5, "description": "Government-run canteen with meals at Rs 5."},
    {"name": "Sri Ayyappa Trust Food Distribution", "category": "food", "address": "T Nagar, Chennai", "city": "Chennai", "lat": 13.0418, "lng": 80.2341, "phone": "044-24343434", "hours": "8AM-8PM", "seats_available": 80, "capacity": 200, "safety_level": 4, "description": "Daily free food distribution."},
    # CHENNAI - Shelter (1)
    {"name": "GCC Night Shelter Egmore", "category": "shelter", "address": "Egmore, Chennai", "city": "Chennai", "lat": 13.0791, "lng": 80.2614, "phone": "044-25383535", "hours": "8PM-6AM", "seats_available": 25, "capacity": 70, "safety_level": 4, "description": "Greater Chennai Corporation night shelter."},
    # KOLKATA - Food (2)
    {"name": "Mother Teresa's Missionaries of Charity", "category": "food", "address": "54A AJC Bose Road, Kolkata", "city": "Kolkata", "lat": 22.5390, "lng": 88.3558, "phone": "033-22490115", "hours": "7AM-11AM", "seats_available": 100, "capacity": 300, "safety_level": 5, "description": "World-famous charity providing free meals."},
    {"name": "Ramakrishna Mission Food Distribution", "category": "food", "address": "Belur Math, Howrah, Kolkata", "city": "Kolkata", "lat": 22.6283, "lng": 88.3541, "phone": "033-26542144", "hours": "11AM-2PM", "seats_available": 150, "capacity": 500, "safety_level": 5, "description": "Daily free meal distribution."},
    # KOLKATA - Shelter (1)
    {"name": "Nishchoy Night Shelter Kolkata", "category": "shelter", "address": "Park Street, Kolkata", "city": "Kolkata", "lat": 22.5517, "lng": 88.3512, "phone": "033-22901234", "hours": "7PM-7AM", "seats_available": 30, "capacity": 80, "safety_level": 3, "description": "Municipal night shelter near Park Street."},
    # HYDERABAD - Food (2)
    {"name": "GHMC Annapurna Canteen", "category": "food", "address": "Charminar Area, Hyderabad", "city": "Hyderabad", "lat": 17.3616, "lng": 78.4747, "phone": "040-23261234", "hours": "7AM-9PM", "seats_available": 90, "capacity": 250, "safety_level": 5, "description": "GHMC canteen providing meals at Rs 5."},
    {"name": "Siasat Daily Food Drive", "category": "food", "address": "Abids, Hyderabad", "city": "Hyderabad", "lat": 17.3950, "lng": 78.4867, "phone": "9000000001", "hours": "6PM-9PM", "seats_available": 60, "capacity": 150, "safety_level": 4, "description": "Free food distribution every evening."},
    # HYDERABAD - Shelter (1)
    {"name": "GHMC Night Shelter Secunderabad", "category": "shelter", "address": "Secunderabad Railway Station Area, Hyderabad", "city": "Hyderabad", "lat": 17.4399, "lng": 78.4983, "phone": "040-27819999", "hours": "8PM-8AM", "seats_available": 20, "capacity": 60, "safety_level": 3, "description": "Municipal night shelter near railway station."},
    # PUNE - Food (2)
    {"name": "Swadhar Greh Food Center", "category": "food", "address": "Koregaon Park, Pune", "city": "Pune", "lat": 18.5362, "lng": 73.8938, "phone": "020-26151234", "hours": "8AM-8PM", "seats_available": 50, "capacity": 150, "safety_level": 4, "description": "Free nutritious meals for homeless."},
    {"name": "ISKCON Pune Prasadam", "category": "food", "address": "Camp Area, Pune", "city": "Pune", "lat": 18.5204, "lng": 73.8567, "phone": "020-26130000", "hours": "11AM-2PM", "seats_available": 70, "capacity": 200, "safety_level": 5, "description": "Daily free prasadam distribution."},
    # PUNE - Shelter (1)
    {"name": "PMC Night Shelter Pune", "category": "shelter", "address": "Near Pune Railway Station", "city": "Pune", "lat": 18.5295, "lng": 73.8744, "phone": "020-25503685", "hours": "8PM-6AM", "seats_available": 25, "capacity": 70, "safety_level": 3, "description": "Pune Municipal Corporation night shelter."},
    # Medical (2)
    {"name": "AIIMS Delhi OPD Free Clinic", "category": "medical", "address": "Ansari Nagar, New Delhi", "city": "Delhi", "lat": 28.5672, "lng": 77.2100, "phone": "011-26588500", "hours": "8AM-4PM Mon-Sat", "seats_available": 50, "capacity": 200, "safety_level": 5, "description": "Free OPD for homeless and underprivileged."},
    {"name": "Victoria Hospital Free Clinic Bengaluru", "category": "medical", "address": "Fort Road, Bengaluru", "city": "Bengaluru", "lat": 12.9615, "lng": 77.5742, "phone": "080-22975300", "hours": "8AM-6PM", "seats_available": 40, "capacity": 100, "safety_level": 5, "description": "Government hospital with free treatment."},
]

VOLUNTEERS = [
    {"name": "Priya Sharma", "phone": "9811000001", "email": "priya@example.com", "skill": "food_delivery", "city": "Delhi", "available_days": "Sat,Sun"},
    {"name": "Rahul Verma", "phone": "9822000002", "email": "rahul@example.com", "skill": "shelter_assistance", "city": "Mumbai", "available_days": "Fri,Sat,Sun"},
    {"name": "Anita Nair", "phone": "9833000003", "email": "anita@example.com", "skill": "medical_aid", "city": "Bengaluru", "available_days": "Sat"},
    {"name": "Mohammed Ali", "phone": "9844000004", "email": "ali@example.com", "skill": "transport", "city": "Hyderabad", "available_days": "Mon,Wed,Fri"},
    {"name": "Kavitha Reddy", "phone": "9855000005", "email": "kavitha@example.com", "skill": "counselling", "city": "Chennai", "available_days": "Tue,Thu,Sat"},
    {"name": "Suresh Kumar", "phone": "9866000006", "email": "suresh@example.com", "skill": "general", "city": "Kolkata", "available_days": "Weekends"},
    {"name": "Deepa Menon", "phone": "9877000007", "email": "deepa@example.com", "skill": "clothing", "city": "Pune", "available_days": "Sun"},
]

class Command(BaseCommand):
    help = 'Seed database with 30 verified locations and sample volunteers'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding locations...')
        Location.objects.all().delete()
        for data in LOCATIONS:
            Location.objects.create(is_verified=True, **data)
        self.stdout.write(self.style.SUCCESS(f'Created {len(LOCATIONS)} locations'))

        Volunteer.objects.all().delete()
        for v in VOLUNTEERS:
            Volunteer.objects.create(**v)
        self.stdout.write(self.style.SUCCESS(f'Created {len(VOLUNTEERS)} volunteers'))

        # Create admin user
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@survivalmap.in', 'admin123')
            self.stdout.write(self.style.SUCCESS('Admin user: admin / admin123'))

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
