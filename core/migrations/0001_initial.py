from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('category', models.CharField(choices=[('food','Food'),('shelter','Shelter'),('water','Water'),('medical','Medical'),('clothing','Clothing')], max_length=20)),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=50)),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('hours', models.CharField(default='24/7', max_length=100)),
                ('seats_available', models.IntegerField(default=0)),
                ('capacity', models.IntegerField(default=100)),
                ('safety_level', models.IntegerField(default=3)),
                ('is_verified', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='location_images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(blank=True)),
                ('skill', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('available_days', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('registered_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmergencyRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('urgency_score', models.IntegerField(default=1)),
                ('urgency_label', models.CharField(max_length=50)),
                ('needs', models.CharField(max_length=200)),
                ('contact', models.CharField(blank=True, max_length=100)),
                ('location_hint', models.CharField(blank=True, max_length=200)),
                ('is_resolved', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='core.location')),
                ('reviewer_name', models.CharField(max_length=100)),
                ('rating', models.IntegerField(default=3)),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShelterVisit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visits', to='core.location')),
                ('day_of_week', models.IntegerField()),
                ('hour', models.IntegerField()),
                ('occupancy_percent', models.FloatField()),
                ('recorded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SMSRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=20)),
                ('message', models.TextField()),
                ('response_sent', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('is_read', models.BooleanField(default=False)),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.location')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
