#!/usr/bin/env python3
"""
Start the pure Python FastAPI server directly
"""
import os
import sys

# Add the python_backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'python_backend'))

if __name__ == "__main__":
    print("🚀 Starting Pure Python Hotel Audit Platform")
    print("=" * 50)
    print("🐍 Python FastAPI Server Starting...")
    print("🗄️ Database: SQLite (hotel_audit.db)")
    print("🌐 Server will run on: http://0.0.0.0:5000")
    print("📝 API Documentation: http://0.0.0.0:5000/docs")
    
    # Change to python_backend directory
    os.chdir('python_backend')
    
    # Import and run the main app
    from main import app
    import uvicorn
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=5000,
        reload=False,
        log_level="info"
    )