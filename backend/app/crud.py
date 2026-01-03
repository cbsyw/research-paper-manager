from sqlalchemy.orm import Session
from app import models, schemas

def get_papers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Paper).offset(skip).limit(limit).all()

def get_paper(db: Session, paper_id: int):
    return db.query(models.Paper).filter(models.Paper.id == paper_id).first()

def create_paper(db: Session, paper: schemas.PaperCreate):
    db_paper = models.Paper(**paper.model_dump())
    db.add(db_paper)
    db.commit()
    db.refresh(db_paper)
    return db_paper

def update_paper(db: Session, paper_id: int, paper: schemas.PaperUpdate):
    db_paper = db.query(models.Paper).filter(models.Paper.id == paper_id).first()
    if db_paper:
        update_data = paper.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_paper, key, value)
        db.commit()
        db.refresh(db_paper)
    return db_paper

def delete_paper(db: Session, paper_id: int):
    db_paper = db.query(models.Paper).filter(models.Paper.id == paper_id).first()
    if db_paper:
        db.delete(db_paper)
        db.commit()
    return db_paper
