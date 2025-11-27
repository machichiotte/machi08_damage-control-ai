from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import shutil
import uuid
from datetime import datetime
import traceback
from services.depth_estimator import get_depth_estimator
from services.object_detector import get_object_detector

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

# Servir les fichiers statiques (images uploadées et depth maps)
app.mount("/files", StaticFiles(directory=str(UPLOAD_DIR)), name="files")


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
        "url": f"/files/{unique_filename}",
        "uploaded_at": datetime.now().isoformat(),
        "message": "Image uploadée avec succès",
    }


@app.post("/analyze/{filename}")
async def analyze_image(filename: str):
    """
    Analyse une image uploadée et génère une depth map
    """
    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Image non trouvée")

    try:
        print(f"📊 Début de l'analyse pour: {filename}")

        # Obtenir l'estimateur de profondeur
        estimator = get_depth_estimator()
        print("✓ Estimateur obtenu")

        # Générer la depth map
        result = estimator.estimate_depth(file_path)
        print("✓ Depth map générée")

        return {
            "status": "success",
            "original_image": f"/files/{filename}",
            "depth_map": f"/files/{result['depth_map_filename']}",
            "stats": result["stats"],
            "device_used": result["device_used"],
            "message": "Analyse de profondeur terminée",
        }
    except Exception as e:
        # Afficher l'erreur complète dans les logs
        print("❌ ERREUR lors de l'analyse:")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500, detail=f"Erreur lors de l'analyse: {str(e)}"
        )


@app.post("/detect/{filename}")
async def detect_objects(filename: str):
    """
    Détecte les objets dans une image uploadée avec YOLO
    """
    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Image non trouvée")

    try:
        print(f"🔍 Début de la détection d'objets pour: {filename}")

        # Obtenir le détecteur d'objets
        detector = get_object_detector()
        print("✓ Détecteur obtenu")

        # Détecter les objets
        result = detector.detect_objects(file_path)
        print(f"✓ {result['stats']['total_objects']} objets détectés")

        return {
            "status": "success",
            "original_image": f"/files/{filename}",
            "annotated_image": f"/files/{result['annotated_image_filename']}",
            "detections": result["detections"],
            "stats": result["stats"],
            "message": "Détection d'objets terminée",
        }
    except Exception as e:
        # Afficher l'erreur complète dans les logs
        print("❌ ERREUR lors de la détection:")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500, detail=f"Erreur lors de la détection: {str(e)}"
        )


@app.post("/detect/parts/{filename}")
async def detect_parts(filename: str):
    """
    Détecte les pièces spécifiques (Zero-Shot) avec OWL-ViT
    """
    from services.zero_shot_detector import get_zero_shot_detector

    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Image non trouvée")

    try:
        print(f"🔍 Début de la détection de pièces pour: {filename}")

        # Obtenir le détecteur Zero-Shot
        detector = get_zero_shot_detector()
        print("✓ Détecteur OWL-ViT obtenu")

        # Détecter les pièces
        result = detector.detect_parts(file_path)
        print(f"✓ {result['stats']['total_objects']} pièces détectées")

        return {
            "status": "success",
            "original_image": f"/files/{filename}",
            "annotated_image": f"/files/{result['annotated_image_filename']}",
            "detections": result["detections"],
            "stats": result["stats"],
            "message": "Détection de pièces terminée",
        }
    except Exception as e:
        print("❌ ERREUR lors de la détection de pièces:")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500, detail=f"Erreur lors de la détection: {str(e)}"
        )
