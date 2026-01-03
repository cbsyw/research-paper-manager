from fastapi import FastAPI
from app.database import engine, Base
from app.routers import papers, search

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Research Paper Manager")

# Include routers
app.include_router(papers.router)
app.include_router(search.router)

@app.get("/")
def read_root():
    return {"message": "Research Paper Manager API - Phase 3"}
