from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from app.routes import scan, health


def create_app() -> FastAPI:
    app = FastAPI(
        title="QR Payment Security API",
        description="Detects fraudulent and tampered UPI QR codes",
        version="1.0.0"
    )

    # CORS (for frontend)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routes
    app.include_router(health.router, prefix="/health", tags=["Health"])
    app.include_router(scan.router, prefix="/api/v1", tags=["QR Scan"])

    return app


# Create app
app = create_app()


# Root endpoint (ONLY ONCE)
@app.get("/")
def root():
    return {
        "project": "QR Payment Security System",
        "status": "Backend running successfully ✅",
        "docs": "http://127.0.0.1:8000/docs"
    }