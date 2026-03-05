from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers import upload, summarize, ask

app = FastAPI(
    title="UltimateRAG Document Intelligence",
    description="Multi-format RAG API with hybrid processing for text and tabular data",
    version="1.0.0",
)

# Add CORS middleware (good practice for APIs)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router, tags=["Upload"])
app.include_router(summarize.router, tags=["Summarize"])
app.include_router(ask.router, tags=["Ask"])

@app.get("/health", tags=["Health"])
def health_check():
    """Simple health check endpoint"""
    return {"status": "ok"}
