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
from services.zero_shot_detector import get_zero_shot_detector
from services.contract_extractor import get_contract_extractor
from services.contract_analyzer import get_contract_analyzer
from services.claim_evaluator import get_claim_evaluator

import os

app = FastAPI(title="DamageControl AI API")

# Configuration CORS pour permettre les requêtes depuis le frontend
allowed_origins = [
    "http://localhost:5173",  # Développement local
    "http://localhost:3000",  # Alternative
    "https://damage-control-ai.netlify.app",  # Production
]

# Ajouter l'URL du frontend en production si définie via variable d'environnement
frontend_url = os.getenv("FRONTEND_URL")
if frontend_url and frontend_url not in allowed_origins:
    allowed_origins.append(frontend_url)
    print(f"✅ CORS: Frontend URL ajoutée: {frontend_url}")

print(f"🔧 CORS: Origines autorisées: {allowed_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
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
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "status": "success",
        "filename": unique_filename,
        "url": f"/files/{unique_filename}",
        "size": file_path.stat().st_size,
        "uploaded_at": datetime.now().isoformat(),
    }


@app.post("/upload/contract")
async def upload_contract(file: UploadFile = File(...)):
    """
    Upload un contrat d'assurance (PDF ou image) pour extraction de texte
    """
    from services.contract_extractor import get_contract_extractor

    # Vérifier le type de fichier
    allowed_types = ["application/pdf", "image/jpeg", "image/png", "image/jpg"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Le fichier doit être un PDF ou une image (JPG, PNG)",
        )

    # Générer un nom de fichier unique
    file_extension = Path(file.filename).suffix
    unique_filename = f"contract_{uuid.uuid4()}{file_extension}"
    file_path = UPLOAD_DIR / unique_filename

    try:
        # Sauvegarder le fichier
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print(f"📄 Contrat uploadé: {unique_filename}")

        # Extraire le texte
        extractor = get_contract_extractor()
        extraction_result = extractor.extract_text(file_path)

        return {
            "status": "success",
            "filename": unique_filename,
            "url": f"/files/{unique_filename}",
            "size": file_path.stat().st_size,
            "uploaded_at": datetime.now().isoformat(),
            "extraction": extraction_result,
            "message": "Contrat uploadé et texte extrait avec succès",
        }
    except Exception as e:
        # Supprimer le fichier en cas d'erreur
        if file_path.exists():
            file_path.unlink()
        print(f"❌ Erreur lors de l'upload du contrat: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500, detail=f"Erreur lors de l'extraction: {str(e)}"
        )


@app.post("/analyze/contract/{filename}")
async def analyze_contract(filename: str):
    """
    Analyse un contrat uploadé pour extraire franchise, plafond et garanties
    """
    from services.contract_extractor import get_contract_extractor
    from services.contract_analyzer import get_contract_analyzer

    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Contrat non trouvé")

    try:
        print(f"📋 Début de l'analyse du contrat: {filename}")

        # Extraire le texte
        extractor = get_contract_extractor()
        extraction_result = extractor.extract_text(file_path)

        # Analyser le contrat
        analyzer = get_contract_analyzer()
        analysis_result = analyzer.analyze_contract(extraction_result["text"])

        print(f"✓ Analyse terminée")

        return {
            "status": "success",
            "filename": filename,
            "extraction": extraction_result,
            "analysis": analysis_result,
            "message": "Analyse du contrat terminée",
        }
    except Exception as e:
        print("❌ ERREUR lors de l'analyse du contrat:")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500, detail=f"Erreur lors de l'analyse: {str(e)}"
        )


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


@app.post("/evaluate/claim")
async def evaluate_claim(
    image_filename: str, contract_filename: str, damage_type: str = "accident"
):
    """
    Évalue si un sinistre est couvert par le contrat

    Args:
        image_filename: Nom du fichier image analysé
        contract_filename: Nom du fichier contrat analysé
        damage_type: Type de sinistre (accident, vol, incendie, etc.)
    """
    try:
        print(f"\n🔍 Évaluation du sinistre:")
        print(f"  - Image: {image_filename}")
        print(f"  - Contrat: {contract_filename}")
        print(f"  - Type: {damage_type}")

        # 1. Charger les données d'analyse d'image
        image_path = UPLOAD_DIR / image_filename
        if not image_path.exists():
            raise HTTPException(status_code=404, detail="Image non trouvée")

        # Récupérer les détections de pièces de voiture
        detector = get_zero_shot_detector()
        detection_result = detector.detect_parts(image_path)

        # Récupérer les stats de profondeur (si disponibles)
        depth_estimator = get_depth_estimator()
        depth_result = depth_estimator.estimate_depth(image_path)

        # Construire les données de dégâts
        damage_data = {
            "detected_objects": detection_result.get("detections", []),
            "depth_stats": depth_result.get("stats", {}),
        }

        # 2. Charger les données du contrat
        contract_path = UPLOAD_DIR / contract_filename
        if not contract_path.exists():
            raise HTTPException(status_code=404, detail="Contrat non trouvé")

        # Extraire et analyser le contrat
        extractor = get_contract_extractor()
        extraction_result = extractor.extract_text(contract_path)

        analyzer = get_contract_analyzer()
        contract_data = analyzer.analyze_contract(extraction_result["text"])

        # 3. Évaluer le sinistre
        evaluator = get_claim_evaluator()
        evaluation = evaluator.evaluate_claim(
            damage_data=damage_data,
            contract_data=contract_data,
            damage_type=damage_type,
        )

        print(f"✅ Évaluation terminée")

        return {
            "status": "success",
            "evaluation": evaluation,
            "image_filename": image_filename,
            "contract_filename": contract_filename,
            "damage_type": damage_type,
            "message": "Évaluation du sinistre terminée",
        }

    except HTTPException:
        raise
    except Exception as e:
        print("❌ ERREUR lors de l'évaluation:")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500, detail=f"Erreur lors de l'évaluation: {str(e)}"
        )
