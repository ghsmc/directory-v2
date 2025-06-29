from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os
from dotenv import load_dotenv

from .search.search_engine import YaleSearchEngine
from .data_loader.s3_loader import S3DataLoader
from .models import Base

load_dotenv()

app = FastAPI(title="Yale Network Search API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/yale_network")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class SearchRequest(BaseModel):
    query: str
    limit: Optional[int] = 50
    use_semantic_search: Optional[bool] = True


class SearchResponse(BaseModel):
    query: str
    parsed_query: Dict[str, Any]
    explanation: Dict[str, Any]
    results: List[Dict[str, Any]]
    total_results: int
    sql_query: Optional[str] = None


@app.post("/api/search", response_model=SearchResponse)
async def search(request: SearchRequest, db: Session = Depends(get_db)):
    """Execute a search query"""
    
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")
        
    search_engine = YaleSearchEngine(db, openai_api_key)
    
    try:
        results = search_engine.search(
            query=request.query,
            use_semantic_search=request.use_semantic_search,
            limit=request.limit
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/import-data")
async def import_data(db: Session = Depends(get_db)):
    """Import data from S3"""
    
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    
    if not aws_access_key or not aws_secret_key:
        raise HTTPException(status_code=500, detail="AWS credentials not configured")
        
    loader = S3DataLoader(aws_access_key, aws_secret_key)
    
    try:
        loader.import_to_database(db)
        return {"message": "Data import completed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/update-embeddings")
async def update_embeddings(db: Session = Depends(get_db)):
    """Update profile embeddings"""
    
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")
        
    search_engine = YaleSearchEngine(db, openai_api_key)
    
    try:
        search_engine.update_profile_embeddings()
        return {"message": "Embeddings updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)