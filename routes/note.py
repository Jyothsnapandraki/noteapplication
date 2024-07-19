from fastapi import APIRouter, Request, HTTPException, status, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from bson import ObjectId
from models.note import Note
from schemas.note import noteEntity, notesEntity
from config.db import conn

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Home route
@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    notes_cursor = conn.notes.notes.find({})
    notes_list = [{"id": str(note["_id"]), "title": note["title"], "desc": note["desc"]} for note in notes_cursor]
    return templates.TemplateResponse("index.html", {"request": request, "newDocs": notes_list})

# Get all notes route
@router.get("/get_all_notes")
async def fetch_all_notes():
    notes_cursor = conn.notes.notes.find({})
    return notesEntity(notes_cursor)

# About page route
@router.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

# Add note to db
@router.post("/")
async def create_note(
    title: str = Form(...),
    desc: str = Form(...)
):
    new_note = {"title": title, "desc": desc}
    result = conn.notes.notes.insert_one(new_note)
    return JSONResponse(content={"message": "Note added successfully", "id": str(result.inserted_id)})

# Read a single note by ID
@router.get("/{note_id}")
async def get_note(note_id: str):
    note = conn.notes.notes.find_one({"_id": ObjectId(note_id)})
    if note:
        return noteEntity(note)
    raise HTTPException(status_code=404, detail="Note not found")

# Update a note by ID
@router.put("/{note_id}")
async def modify_note(note_id: str, updated_note: Note):
    result = conn.notes.notes.update_one({"_id": ObjectId(note_id)}, {"$set": updated_note.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Note not found")
    return JSONResponse(content={"message": "Note updated successfully"})

# Delete a note by ID
@router.delete("/{note_id}")
async def remove_note(note_id: str):
    result = conn.notes.notes.delete_one({"_id": ObjectId(note_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Note not found")
    return JSONResponse(content={"message": "Note deleted successfully"})
