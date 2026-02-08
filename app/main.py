"""
Main FastAPI application.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime

from app.core.config import settings
from app.core.database import mongodb, get_database
from app.models.requests import AnalyzeRequest
from app.services.analysis_service import analysis_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting Waypoint API...")
    mongodb.connect()
    yield
    print("👋 Shutting down Waypoint API...")
    mongodb.close()


app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan
)

# ============================================
# CORS Configuration - IMPORTANT!
# This allows your frontend to communicate with the backend
# ============================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # Frontend dev server (Vite default)
        "http://localhost:5173",      # Alternative Vite port
        "http://127.0.0.1:3000",      # Alternative localhost
        "http://127.0.0.1:5173",      # Alternative localhost
        "https://waypoint-pi.vercel.app/",
        "https://*.vercel.app",
        # Add your production frontend URL here when deploying:
        # "https://waypoint.vercel.app",
        # "https://your-custom-domain.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
def read_root():
    return {
        "message": "Waypoint API is running",
        "version": settings.API_VERSION,
        "status": "healthy"
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/analyze")
async def analyze_idea(request: AnalyzeRequest):
    """
    Analyze a product idea.
    """
    try:
        result = await analysis_service.analyze_product(
            product_idea=request.product_idea,
            tier=request.tier,
            email=request.email
        )

        return {
            "success": True,
            "job_id": result["job_id"],
            "data": result
        }

    except Exception as e:
        print(f"❌ API Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/results/{job_id}")
def get_results(job_id: str):
    try:
        db = get_database()
        analysis = db["analyses"].find_one({"job_id": job_id})

        if not analysis:
            return {"success": False, "message": "Analysis not found"}

        analysis["_id"] = str(analysis["_id"])
        return {"success": True, "data": analysis}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/test-db")
def test_database():
    try:
        db = get_database()
        result = db["test"].insert_one({
            "message": "Hello from Waypoint!",
            "timestamp": datetime.utcnow()
        })

        doc = db["test"].find_one({"_id": result.inserted_id})
        doc["_id"] = str(doc["_id"])

        return {"status": "success", "document": doc}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))