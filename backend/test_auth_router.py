#!/usr/bin/env python3
"""
Test script to verify that the auth router can be imported and has the correct endpoints.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

try:
    from src.api.auth import router
    print("SUCCESS: Successfully imported auth router")
    print(f"Router type: {type(router)}")
    print(f"Router routes: {[route.path for route in router.routes]}")

    # Check if login and register routes exist
    paths = [route.path for route in router.routes]
    if '/login' in paths:
        print("SUCCESS: /login route exists")
    else:
        print("ERROR: /login route NOT FOUND")

    if '/register' in paths:
        print("SUCCESS: /register route exists")
    else:
        print("ERROR: /register route NOT FOUND")

except Exception as e:
    print(f"ERROR importing auth router: {e}")
    import traceback
    traceback.print_exc()