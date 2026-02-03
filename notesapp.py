from fastapi import FastAPI, Path, HTTPException
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

app = FastAPI()

engine = create_engine("sqlite:///notes.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class NoteDB(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    todo = Column(String)
    when = Column(String)
    done = Column(Boolean)

Base.metadata.create_all(bind=engine)

class Note(BaseModel):
    todo: str
    when: str
    done: bool

class UpdateNote(BaseModel):
    todo: Optional[str] = None
    when: Optional[str] = None
    done: Optional[bool] = None


@app.get("/")
def index():
    return {"message": "Notes API"}


@app.get("/get-note/{note_id}")
def get_note(note_id: int = Path(gt=0)):
    db = SessionLocal()
    note = db.query(NoteDB).filter(NoteDB.id == note_id).first()
    db.close()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    return note


@app.get("/get-by-todo")
def get_note_by_todo(todo: str):
    db = SessionLocal()
    note = db.query(NoteDB).filter(NoteDB.todo == todo).first()
    db.close()

    if not note:
        raise HTTPException(status_code=404, detail="Not found")

    return note


@app.post("/create-note/{note_id}")
def create_note(note_id: int, note: Note):
    db = SessionLocal()

    existing = db.query(NoteDB).filter(NoteDB.id == note_id).first()
    if existing:
        db.close()
        raise HTTPException(status_code=400, detail="Note already exists")

    new_note = NoteDB(id=note_id, todo=note.todo, when=note.when, done=note.done)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    db.close()

    return new_note


@app.put("/update-note/{note_id}")
def update_note(note_id: int, note: UpdateNote):
    db = SessionLocal()
    existing = db.query(NoteDB).filter(NoteDB.id == note_id).first()

    if not existing:
        db.close()
        raise HTTPException(status_code=404, detail="Note does not exist")

    if note.todo is not None:
        existing.todo = note.todo
    if note.when is not None:
        existing.when = note.when
    if note.done is not None:
        existing.done = note.done

    db.commit()
    db.refresh(existing)
    db.close()

    return existing


@app.delete("/delete-note/{note_id}")
def delete_note(note_id: int):
    db = SessionLocal()
    note = db.query(NoteDB).filter(NoteDB.id == note_id).first()

    if not note:
        db.close()
        raise HTTPException(status_code=404, detail="Note does not exist")

    db.delete(note)
    db.commit()
    db.close()

    return {"message": "note deleted successfully"}
