#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple HTTP Server for Telegram WebApp
Serves the public view page on HTTPS
"""

import http.server
import ssl
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
    """Run the HTTPS server"""
    server_address = ('localhost', 8443)
    
    # Create SSL context (self-signed certificate for testing)
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    
    # For testing, we'll use a simple context without certificate verification
    # In production, you'd use proper SSL certificates
    
    print("🌐 Starting HTTPS Server for Telegram WebApp")
    print("📱 Server running on: https://localhost:8443")
    print("🔗 Public View: https://localhost:8443/public-view.html")
    print("🔗 Dashboard: https://localhost:8443/dashboard")
    print("=" * 50)
    print("📱 Update your bot WebApp URL to: https://localhost:8443/public-view.html")
    print("📱 Then test the WebApp button in Telegram")
    print("=" * 50)
    
    try:
        # Create server
        httpd = http.server.HTTPServer(server_address, CustomHTTPRequestHandler)
        
        # Wrap with SSL
        httpsd = httpd.socketserver.TCPServer(server_address, CustomHTTPRequestHandler)
        httpsd.socket = ssl.wrap_socket(httpd.socket, server_side=True, certfile='server.crt', keyfile='server.key', ssl_version=ssl.PROTOCOL_TLS)
        
        print("🚀 Server started successfully!")
        print("📱 Ready to serve Telegram WebApp!")
        
        # Start server
        httpsd.serve_forever()
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        print("📱 Trying alternative server without SSL...")
        
        # Fallback to HTTP server
        try:
            httpd = http.server.HTTPServer(server_address, CustomHTTPRequestHandler)
            print("🌐 HTTP Server running on: http://localhost:8443")
            print("📱 Update bot URL to: http://localhost:8443/public-view.html")
            httpd.serve_forever()
        except Exception as e2:
            print(f"❌ Alternative server error: {e2}")

if __name__ == '__main__':
    run_server()
