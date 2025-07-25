#!/bin/bash
echo "🚀 Starting Pure Python Hotel Audit Platform"
echo "=" * 50
echo "🐍 Python FastAPI Server Starting..."
echo "🗄️ Database: SQLite (hotel_audit.db)"
echo "🌐 Server will run on: http://0.0.0.0:5000"
echo "📝 API Documentation: http://0.0.0.0:5000/docs"

cd python_backend
python main.py