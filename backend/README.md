---
title: DamageControl AI Backend
emoji: 🚗
colorFrom: purple
colorTo: blue
sdk: docker
pinned: false
license: mit
---

# 🚗 DamageControl AI - Backend API

Backend API pour l'analyse automatique des dommages automobiles par IA.

## 🎯 Fonctionnalités

- **Depth Estimation 3D** : Génération de cartes de profondeur avec Depth Anything
- **Détection d'Objets** : YOLOv8 pour identifier les véhicules et dommages
- **Détection Zero-Shot** : OWL-ViT pour identifier les pièces automobiles
- **Analyse de Contrats** : Extraction de garanties depuis PDF avec PyPDF2 + Tesseract
- **Évaluation de Sinistres** : Croisement des données visuelles et contractuelles

## 🛠 Stack Technique

- **Framework** : FastAPI
- **IA** : Hugging Face Transformers, Ultralytics YOLO
- **Vision** : OpenCV, PIL
- **OCR** : Tesseract, PyPDF2

## 📚 Documentation API

Une fois déployé, accède à la documentation interactive :

- **Swagger UI** : `/docs`
- **ReDoc** : `/redoc`

## 🔗 Frontend

Le frontend est déployé sur Netlify : [https://damage-control-ai.netlify.app](https://damage-control-ai.netlify.app)

## 📝 Endpoints Principaux

- `POST /upload` : Upload d'image
- `POST /analyze/{filename}` : Analyse de profondeur 3D
- `POST /detect/{filename}` : Détection d'objets (YOLO)
- `POST /detect/parts/{filename}` : Détection de pièces (OWL-ViT)
- `POST /upload/contract` : Upload de contrat PDF
- `POST /analyze/contract/{filename}` : Analyse de contrat
- `POST /evaluate/claim` : Évaluation complète de sinistre

## 🚀 Utilisation

```python
import requests

# Upload d'une image
files = {'file': open('car_damage.jpg', 'rb')}
response = requests.post('https://YOUR-SPACE.hf.space/upload', files=files)
filename = response.json()['filename']

# Analyse de profondeur
response = requests.post(f'https://YOUR-SPACE.hf.space/analyze/{filename}')
depth_data = response.json()
```

## 📦 Modèles Utilisés

- **Depth Anything Small** : `LiheYoung/depth-anything-small-hf`
- **YOLOv8 Nano** : `yolov8n.pt`
- **OWL-ViT Base** : `google/owlvit-base-patch32`

## 🔧 Configuration

Variables d'environnement :

- `FRONTEND_URL` : URL du frontend pour CORS (optionnel)
- `PORT` : Port du serveur (défaut: 7860)

## 📄 License

MIT License - Voir [LICENSE](../LICENSE)

## 👨‍💻 Auteur

[@machichiotte](https://github.com/machichiotte)
