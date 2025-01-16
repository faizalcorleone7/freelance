from fastapi import APIRouter, UploadFile, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import asyncio
from concurrent.futures import ThreadPoolExecutor
from services.redis_service import create_index_if_not_exists, process_document, search_documents

router = APIRouter()

executor = ThreadPoolExecutor(max_workers=4)

class SearchQuery(BaseModel):
    query: str
    top_k: Optional[int] = 5

class SearchResult(BaseModel):
    document_id: str
    similarity_score: float
    content: str

@router.on_event("startup")
async def startup_event():
    create_index_if_not_exists()

@router.post("/upload")
async def upload_document(file: UploadFile):
    try:
        content = await file.read()
        content = content.decode("utf-8")
        doc_id = f"doc_{hash(content)}"
        success = await asyncio.get_event_loop().run_in_executor(
            executor,
            process_document,
            content,
            doc_id
        )

        if success:
            return {"message": "Document uploaded successfully", "doc_id": doc_id}
        else:
            raise HTTPException(status_code=500, detail="Failed to process document")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search", response_model=List[SearchResult])
async def search_documents(query: SearchQuery):
    try:
        results = search_documents(query.query, query.top_k)
        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
