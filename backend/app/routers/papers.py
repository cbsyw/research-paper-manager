from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/papers", tags=["papers"])

@router.get("/", response_model=List[schemas.Paper])
def list_papers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    papers = crud.get_papers(db, skip=skip, limit=limit)
    return papers

@router.get("/{paper_id}", response_model=schemas.Paper)
def get_paper(paper_id: int, db: Session = Depends(get_db)):
    paper = crud.get_paper(db, paper_id=paper_id)
    if paper is None:
        raise HTTPException(status_code=404, detail="Paper not found")
    return paper

@router.post("/", response_model=schemas.Paper, status_code=201)
def create_paper(paper: schemas.PaperCreate, db: Session = Depends(get_db)):
    return crud.create_paper(db=db, paper=paper)

@router.put("/{paper_id}", response_model=schemas.Paper)
def update_paper(paper_id: int, paper: schemas.PaperUpdate, db: Session = Depends(get_db)):
    db_paper = crud.update_paper(db=db, paper_id=paper_id, paper=paper)
    if db_paper is None:
        raise HTTPException(status_code=404, detail="Paper not found")
    return db_paper

@router.delete("/{paper_id}", response_model=schemas.Paper)
def delete_paper(paper_id: int, db: Session = Depends(get_db)):
    db_paper = crud.delete_paper(db=db, paper_id=paper_id)
    if db_paper is None:
        raise HTTPException(status_code=404, detail="Paper not found")
    return db_paper
