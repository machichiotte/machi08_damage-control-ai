from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil
import uuid
from datetime import datetime

app = FastAPI(title="DamageControl AI API")

# Configuration CORS pour permettre les requêtes depuis le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Port par défaut de Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Créer le dossier uploads s'il n'existe pas
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.get("/")
def read_root():
    return {"message": "DamageControl AI Backend is running"}


@app.get("/health")
def health_check():
    return {"status": "ok", "upload_dir": str(UPLOAD_DIR.absolute())}


@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    """
    Upload une image de dégât pour analyse
    """
    # Vérifier le type de fichier
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Le fichier doit être une image")

    # Générer un nom de fichier unique
    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = UPLOAD_DIR / unique_filename

    # Sauvegarder le fichier
    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur lors de la sauvegarde: {str(e)}"
        )

    return {
        "filename": unique_filename,
        "original_filename": file.filename,
        "size": file_path.stat().st_size,
        "path": str(file_path),
        "uploaded_at": datetime.now().isoformat(),
        "message": "Image uploadée avec succès",
    }
