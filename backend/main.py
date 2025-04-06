from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database.session import engine, Base
from backend.config import settings
from backend.controllers import (
    auth,
    user,
    media,
    library,
    player,
    subtitle
)

# Create database tables (in production, use Alembic migrations instead)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_PREFIX}/openapi.json"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=settings.API_PREFIX)
app.include_router(user.router, prefix=settings.API_PREFIX)
app.include_router(media.router, prefix=settings.API_PREFIX)
app.include_router(library.router, prefix=settings.API_PREFIX)
app.include_router(player.router, prefix=settings.API_PREFIX)
app.include_router(subtitle.router, prefix=settings.API_PREFIX)

@app.get("/")
def read_root():
    return {"message": "Welcome to WildMediaServer API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="debug"
    )