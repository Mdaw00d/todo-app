#!/usr/bin/env python3
"""
Test script to verify that the simplified main app includes all routes.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

try:
    from main_simple import app
    print("SUCCESS: Successfully imported simplified main app")
    print(f"App type: {type(app)}")

    # Print all routes in the simplified app
    print("All routes in simplified app:")
    for route in app.routes:
        if hasattr(route, 'path'):
            print(f"  - {route.path}")
        else:
            print(f"  - {route.__class__.__name__}: {getattr(route, '__dict__', 'no path attr')}")

    # Check specifically for auth routes
    auth_paths = [route.path for route in app.routes if hasattr(route, 'path') and '/auth' in route.path.lower()]
    print(f"Auth-related paths found: {auth_paths}")

except Exception as e:
    print(f"ERROR importing simplified main app: {e}")
    import traceback
    traceback.print_exc()