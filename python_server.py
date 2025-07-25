#!/usr/bin/env python3
"""
Pure Python FastAPI server for Hotel Audit Platform
This replaces the Express.js backend entirely
"""

import subprocess
import sys
import os

def start_python_server():
    """Start the Python FastAPI server"""
    print("🚀 Starting Pure Python Hotel Audit Platform")
    print("=" * 50)
    print("🐍 Python FastAPI Server Starting...")
    print("🗄️ Database: SQLite (hotel_audit.db)")
    print("🌐 Server will run on: http://0.0.0.0:5000")
    print("📝 API Documentation: http://0.0.0.0:5000/docs")
    
    # Change to python_backend directory
    os.chdir('python_backend')
    
    # Start the FastAPI server
    try:
        subprocess.run([
            sys.executable, 
            "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "5000", 
            "--reload"
        ], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")

if __name__ == "__main__":
    start_python_server()