#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple HTTP Server for Telegram WebApp
Serves the public view page
"""

import http.server
import socketserver
import os
from urllib.parse import urlparse

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=".", **kwargs)
    
    def do_GET(self):
        # Parse the URL
        parsed_path = urlparse(self.path)
        
        # Serve the public view page for root or specific paths
        if parsed_path.path == '/' or parsed_path.path == '/public-view.html':
            self.serve_public_view()
        elif parsed_path.path == '/dashboard':
            self.serve_dashboard()
        else:
            # Try to serve the file normally
            super().do_GET()
    
    def serve_public_view(self):
        """Serve the public view HTML page"""
        try:
            with open('public-view.html', 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
            self.send_error(404, "File not found")
    
    def serve_dashboard(self):
        """Serve the dashboard HTML page"""
        try:
            with open('dashboard/index.html', 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
            self.send_error(404, "Dashboard not found")
    
    def end_headers(self):
        """Add CORS headers for Telegram WebApp"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def run_server():
    """Run the HTTP server"""
    PORT = 8080
    server_address = ('', PORT)
    
    print("🌐 Starting HTTP Server for Telegram WebApp")
    print("📱 Server running on: http://localhost:8080")
    print("🔗 Public View: http://localhost:8080/public-view.html")
    print("🔗 Dashboard: http://localhost:8080/dashboard")
    print("=" * 50)
    print("📱 Update your bot WebApp URL to: http://localhost:8080/public-view.html")
    print("📱 Then test the WebApp button in Telegram")
    print("=" * 50)
    
    try:
        with socketserver.TCPServer(server_address, CustomHTTPRequestHandler) as httpd:
            print(f"🚀 Server started successfully on port {PORT}!")
            print("📱 Ready to serve Telegram WebApp!")
            print("📱 Press Ctrl+C to stop the server")
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")

if __name__ == '__main__':
    run_server()
