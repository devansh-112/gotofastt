#!/usr/bin/env python3
"""
Local Development Server for K-Logi
Run this for local development
"""

import os
import sys
from app import app

if __name__ == '__main__':
    print("🚀 Starting K-Logi Local Development Server...")
    print("📍 Access your app at: http://localhost:5000")
    print("🔧 Admin Panel: http://localhost:5000/admin/login")
    print("👤 Admin Login: admin / admin123")
    print("📱 Partner Login: partner1 / partner123")
    print("\nPress Ctrl+C to stop the server")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    ) 