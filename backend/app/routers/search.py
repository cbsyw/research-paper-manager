from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app import crud, schemas
from app.database import get_db
from app.services import openalex

router = APIRouter(tags=["search"])

class SearchRequest(BaseModel):
    query: str
    limit: int = 10

class AddFromOpenAlexRequest(BaseModel):
    openalex_id: str
    notes: str = ""

@router.post("/search")
async def search_openalex(request: SearchRequest):
    """
    Search for papers in OpenAlex database.

    Returns list of papers matching the search query.
    """
    try:
        papers = await openalex.search_papers(request.query, request.limit)
        return {"results": papers, "count": len(papers)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/papers/from-openalex", response_model=schemas.Paper, status_code=201)
async def add_paper_from_openalex(request: AddFromOpenAlexRequest, db: Session = Depends(get_db)):
    """
    Fetch a paper from OpenAlex and add it to your library.

    Args:
        openalex_id: The OpenAlex ID of the paper (e.g., https://openalex.org/W...)
        notes: Optional notes to add to the paper
    """
    try:
        # Fetch paper details from OpenAlex
        paper_data = await openalex.get_paper_by_id(request.openalex_id)

        if not paper_data:
            raise HTTPException(status_code=404, detail="Paper not found in OpenAlex")

        # Create paper in our database
        paper_create = schemas.PaperCreate(
            title=paper_data["title"],
            authors=paper_data["authors"],
            year=paper_data["year"],
            abstract=paper_data.get("abstract"),
            url=paper_data["url"],
            notes=request.notes
        )

        db_paper = crud.create_paper(db=db, paper=paper_create)
        return db_paper

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
