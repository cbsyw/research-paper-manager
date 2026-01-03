from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import papers, search

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Research Paper Manager")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(papers.router)
app.include_router(search.router)

@app.get("/")
def read_root():
    return {"message": "Research Paper Manager API - Phase 3"}
