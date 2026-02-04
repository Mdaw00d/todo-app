from fastapi import FastAPI
from src.api.auth import router as auth_router

app = FastAPI(title="Test App")
app.include_router(auth_router)

# Add a simple test endpoint
@app.get("/test")
def test_endpoint():
    return {"message": "Test endpoint works"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)