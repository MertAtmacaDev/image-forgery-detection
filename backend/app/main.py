import os
import shutil
from fastapi import FastAPI, File, UploadFile, HTTPException
import uuid

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "api is working"}

upload_dir = "uploads"

os.makedirs(upload_dir, exist_ok=True)

allowed_extensions = {"jpeg", "jpg", "png", "gif", "bmp", "tiff"}

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    extension = file.filename.split(".")[-1].lower()

    if extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid file extension")
    
    unique_filename = f"{uuid.uuid4()}.{extension}"
    file_path = os.path.join(upload_dir, unique_filename)

    with open(file_path, "wb") as buffer:#save file
        shutil.copyfileobj(file.file, buffer)

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": os.path.getsize(file_path),
        "unique_filename": unique_filename
    }