from fastapi import FastAPI, Path
from typing import Optional 
from pydantic import BaseModel

app = FastAPI()

notes = {
    1: {
        "todo": "Buy groceries",
        "when": "2024-02-01",
        "done": False
    },
    2: {
        "todo": "Complete project",
        "when": "2024-02-05",
        "done": True
    }
}

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
def get_note(
    note_id: int = Path(description="The ID of the note you want to view", gt=0)
):
    return notes[note_id]

@app.get("/get-by-todo")
def get_note_by_todo(todo: str):
    for note_id in notes:
        if notes[note_id]["todo"] == todo:
            return notes[note_id]
    return {"data": "not found"}

@app.post("/create-note/{note_id}")
def create_note(note_id: int, note: Note):
    if note_id in notes:
        return {"error": "note already exists"}
    
    notes[note_id] = note.dict()
    return notes[note_id]

@app.put("/update-note/{note_id}")
def update_note(note_id: int, note: UpdateNote):
    if note_id not in notes:
        return {"error": "note does not exist"}
    
    if note.todo is not None:
        notes[note_id]["todo"] = note.todo
    if note.when is not None:
        notes[note_id]["when"] = note.when
    if note.done is not None:
        notes[note_id]["done"] = note.done
    
    return notes[note_id]

@app.delete("/delete-note/{note_id}")
def delete_note(note_id: int):
    if note_id not in notes:
        return {"error": "note does not exist"}
    
    del notes[note_id]
    return {"message": "note deleted successfully"}