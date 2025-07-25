#!/usr/bin/env python3
"""
Simple HTTP server to serve React frontend and proxy API calls to Python backend
Pure Python architecture - no Express/Node.js dependencies
"""
import http.server
import urllib.request
import urllib.parse
import json
import os
import sys
import subprocess
import threading
import time

class ProxyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="client", **kwargs)
    
    def do_GET(self):
        if self.path.startswith('/api/'):
            self.proxy_to_backend()
        else:
            # Serve React frontend files
            if self.path == '/':
                self.path = '/index.html'
            elif not self.path.startswith('/src/') and not '.' in os.path.basename(self.path):
                # SPA routing - serve index.html for routes
                self.path = '/index.html'
            super().do_GET()
    
    def do_POST(self):
        if self.path.startswith('/api/'):
            self.proxy_to_backend()
        else:
            super().do_POST()
    
    def proxy_to_backend(self):
        """Proxy API requests to Python FastAPI backend"""
        try:
            # Read request body for POST requests
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length > 0 else b''
            
            # Build backend URL
            backend_url = f"http://localhost:8000{self.path}"
            
            # Create request
            req = urllib.request.Request(
                backend_url,
                data=body if body else None,
                headers={'Content-Type': 'application/json'}
            )
            req.get_method = lambda: self.command
            
            # Send request to backend
            with urllib.request.urlopen(req) as response:
                # Send response back to client
                self.send_response(response.getcode())
                for header, value in response.headers.items():
                    if header.lower() not in ['connection', 'transfer-encoding']:
                        self.send_header(header, value)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                # Stream response body
                while True:
                    chunk = response.read(8192)
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    
        except Exception as e:
            print(f"Proxy error: {e}")
            self.send_error(502, f"Backend proxy error: {e}")

def start_python_backend():
    """Start the Python FastAPI backend server"""
    print("🐍 Starting Python FastAPI backend server...")
    os.chdir('python_backend')
    subprocess.Popen([sys.executable, 'main.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    os.chdir('..')
    time.sleep(3)  # Give backend time to start

def start_frontend_server():
    """Start the frontend proxy server"""
    print("🌐 Starting frontend server with API proxy...")
    server = http.server.HTTPServer(('0.0.0.0', 5000), ProxyHTTPRequestHandler)
    print("✅ Server running on http://0.0.0.0:5000")
    print("📱 Frontend: http://0.0.0.0:5000")
    print("🔗 API Proxy: http://0.0.0.0:5000/api/* -> http://localhost:8000/api/*")
    server.serve_forever()

if __name__ == "__main__":
    print("🚀 Hotel Audit Platform - Pure Python Architecture")
    print("=" * 55)
    print("🗄️ Database: SQLite")
    print("🐍 Backend: Python FastAPI")
    print("⚛️  Frontend: React TypeScript")
    print("🌐 Server: Python HTTP Server")
    
    # Start backend in separate thread
    backend_thread = threading.Thread(target=start_python_backend, daemon=True)
    backend_thread.start()
    
    # Start frontend server
    try:
        start_frontend_server()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")