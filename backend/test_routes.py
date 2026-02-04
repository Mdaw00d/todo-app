from src.main import app

print("Registered routes:")
for route in app.routes:
    if hasattr(route, 'methods') and hasattr(route, 'path'):
        print(f"{route.methods} {route.path}")
    else:
        print(f"Route: {route}")

print("\nSpecific auth routes:")
for route in app.routes:
    if 'auth' in getattr(route, 'path', ''):
        print(f"{getattr(route, 'methods', 'N/A')} {getattr(route, 'path', 'N/A')}")