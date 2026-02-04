from fastapi import FastAPI
from src.api.auth import router as auth_router

app = FastAPI()
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Debug auth server", "routes": [route.path for route in app.routes]}