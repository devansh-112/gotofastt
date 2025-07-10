#!/usr/bin/env python3
"""
Production Server for K-Logi
Run this for production deployment
"""

import os
import sys
import subprocess
from app import app

if __name__ == '__main__':
    print("🚀 Starting K-Logi Production Server...")
    print("📍 Server will be available on the configured port")
    print("🔧 Admin Panel: /admin/login")
    print("👤 Admin Login: admin / admin123")
    print("📱 Partner Login: partner1 / partner123")
    
    # Use Gunicorn for production
    port = int(os.environ.get("PORT", 8000))
    
    cmd = [
        "gunicorn",
        "--bind", f"0.0.0.0:{port}",
        "--workers", "4",
        "--timeout", "120",
        "--max-requests", "1000",
        "--max-requests-jitter", "100",
        "wsgi:app"
    ]
    
    print(f"🌐 Starting server on port {port}")
    print(f"🔧 Command: {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}") 