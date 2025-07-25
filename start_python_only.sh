#!/bin/bash

echo "🚀 Starting Hotel Audit System - Python Backend Only"
echo "=================================================="

# Kill any existing processes on port 8000
echo "🔧 Cleaning up existing processes..."
pkill -f "python.*main.py" || true
pkill -f "uvicorn" || true

# Wait a moment for processes to clean up
sleep 2

# Start Python backend
echo "🐍 Starting Python FastAPI backend on port 8000..."
cd python_backend
python main.py &
PYTHON_PID=$!

echo "✅ Python backend started with PID: $PYTHON_PID"
echo "🌐 Backend API: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo "🔍 Health Check: http://localhost:8000/health"
echo ""
echo "🛠️  Frontend should be configured to connect to port 8000"
echo "⏹️  Press Ctrl+C to stop the server"

# Wait for the Python process
wait $PYTHON_PID