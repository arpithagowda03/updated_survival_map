#!/bin/bash
echo ""
echo "╔══════════════════════════════════════════╗"
echo "║     SurvivalMap v5 — Setup Script        ║"
echo "╚══════════════════════════════════════════╝"
echo ""
echo "📦 Installing dependencies..."
pip install django djangorestframework Pillow

echo "🗃  Running migrations..."
python manage.py migrate --run-syncdb

echo "🌱 Seeding 30 locations + volunteers..."
python manage.py seed_data

echo ""
echo "✅ Setup complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🌐 Home      →  http://127.0.0.1:8000/"
echo "  🗺  User Map  →  http://127.0.0.1:8000/map/"
echo "  🔐 Admin     →  http://127.0.0.1:8000/login/"
echo "  👤 Login     →  admin / admin123"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🚀 Starting server..."
python manage.py runserver
