import os
import shutil
import uuid
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from routers.analysis import router as analysis_router
from routers.ai_analysis import router as ai_analysis_router

app = FastAPI(title="Image Forgery Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../uploads"))
os.makedirs(UPLOAD_DIR, exist_ok=True)

allowed_extensions = {"jpeg", "jpg", "png", "gif", "bmp", "tiff"}

@app.get("/")
async def root():
    return {"message": "Api is working."}

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    extension = file.filename.split(".")[-1].lower()

    if extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Geçersiz dosya uzantısı.")
    
    unique_filename = f"{uuid.uuid4()}.{extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": os.path.getsize(file_path),
        "unique_filename": unique_filename
    }

app.include_router(analysis_router)
app.include_router(ai_analysis_router)