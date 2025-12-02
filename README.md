# DamageControl AI - L'Expert en Sinistres Automatisé

[![GitHub](https://img.shields.io/badge/GitHub-machichiotte%2Fdamage--control--ai-blue?logo=github)](https://github.com/machichiotte/damage-control-ai)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![Netlify Status](https://api.netlify.com/api/v1/badges/YOUR_SITE_ID/deploy-status)](https://app.netlify.com/sites/damage-control-ai/deploys)

## 🌐 Démo en Ligne

🚀 **Application** : [https://damage-control-ai.netlify.app](https://damage-control-ai.netlify.app)  
📚 **Documentation API** : [https://damage-control-ai-backend.onrender.com/docs](https://damage-control-ai-backend.onrender.com/docs)

> ⚠️ **Note** : Le backend (plan gratuit Render) s'endort après 15 min d'inactivité. Premier chargement : ~30 secondes.

## 🎯 Concept

DamageControl AI est une Progressive Web App (PWA) révolutionnaire qui automatise l'évaluation des dommages automobiles et domestiques. En utilisant l'intelligence artificielle pour l'analyse d'images (profondeur, segmentation, détection) et le traitement du langage naturel (analyse de contrats), elle accélère le processus de déclaration de sinistre (FNOL) et réduit la fraude.

## ✨ Fonctionnalités Actuelles

### ✅ Implémenté

1.  **Upload d'Images Interactif** 📸

    - Drag & drop ou sélection de fichier
    - Prévisualisation instantanée
    - Interface moderne avec animations

2.  **Depth Estimation (Vision 3D)** 🎯

    - Analyse de la gravité des impacts via des cartes de profondeur
    - Modèle IA : Depth Anything (Hugging Face)
    - Visualisation côte à côte (original vs depth map)
    - Statistiques de profondeur (min/max/moyenne)
    - Colormap INFERNO pour meilleure lisibilité

3.  **Visualisation 3D Interactive** 🧊

    - Affichage 3D de la depth map avec TresJS
    - Rotation automatique et manuelle (OrbitControls)
    - Zoom et pan interactifs
    - Displacement mapping pour relief 3D réel

4.  **Object Detection (YOLO)** 🔍

    - Détection d'objets génériques (voitures, personnes, camions)
    - Modèle : YOLOv8 nano
    - Bounding boxes avec scores de confiance
    - Statistiques de détection

5.  **Zero-Shot Object Detection (OWL-ViT)** 🧩

    - Détection de pièces spécifiques sans entraînement
    - Modèle : OWL-ViT (Google)
    - Détecte : bumper, door, wheel, tire, headlight, hood, etc.
    - Requêtes textuelles personnalisables

6.  **Analyse de Contrat (NLP)** 📄

    - Upload de contrats d'assurance (PDF/Images)
    - Extraction automatique de texte (PyPDF2 + Tesseract OCR)
    - Analyse par regex pour détecter :
      - Franchises
      - Plafonds de garantie
      - Types de garanties (Vol, Incendie, Bris de glace, etc.)
    - Interface dédiée avec visualisation des résultats

7.  **Logique Métier (Évaluation de Sinistre)** 🧠
    - Service `ClaimEvaluator` pour croiser analyse visuelle et contractuelle
    - Calcul automatique du coût estimé basé sur les pièces détectées
    - Décision automatique : "Sinistre Couvert : OUI/NON"
    - Calcul du remboursement (coût estimé - franchise)
    - Interface complète avec détails financiers et dégâts détectés

### 🔄 En Cours (Sprint 4 - 50%)

8.  **UI/UX Premium** 🎨
    - [x] Design Dark Mode futuriste avec Glassmorphism
    - [x] Animations de chargement pendant le traitement IA
    - [x] Système d'onglets pour navigation (Image / Contrat)
    - [ ] Galerie des analyses précédentes
    - [ ] PWA (installable sur mobile)
    - [ ] Optimisations performances

## 🛠 Stack Technique

- **Frontend** : Vue.js 3 (Vite) + TailwindCSS + TresJS
- **Backend** : Python (FastAPI)
- **IA/ML** : Hugging Face Transformers + Ultralytics
  - Depth Anything (depth estimation) ✅
  - YOLOv8 (object detection) ✅
  - OWL-ViT (zero-shot detection) ✅
  - TAPAS (table QA) 🔄
- **Stockage** : Local (fichiers) pour le développement
- **Déploiement** : Prévu sur Vercel (frontend) + Railway (backend)

## 📂 Structure du Projet

```
/damage_control_ai
├── /frontend          # Application Vue.js
│   ├── /src
│   │   ├── /components
│   │   │   ├── ImageUploader.vue    # Composant d'upload
│   │   │   └── DepthViewer3D.vue    # Visualisation 3D
│   │   ├── App.vue
│   │   └── main.js
│   └── package.json
├── /backend           # API FastAPI
│   ├── main.py        # Endpoints REST
│   ├── /services
│   │   ├── depth_estimator.py       # Depth Anything
│   │   ├── object_detector.py       # YOLO
│   │   └── zero_shot_detector.py    # OWL-ViT
│   └── requirements.txt
└── /docs              # Documentation
    ├── ARCHITECTURE.md
    ├── SPRINTS.md
    └── SETUP.md
```

## 🏁 Démarrage Rapide

### Prérequis

- Node.js 18+
- Python 3.9+
- ~4GB d'espace disque (modèles IA)

### Installation

**Frontend :**

```bash
cd frontend
npm install
npm run dev
```

👉 Frontend accessible sur http://localhost:5173

**Backend :**

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

👉 Backend accessible sur http://127.0.0.1:8000

⚠️ **Note :** Au premier lancement, les modèles IA seront téléchargés :

- Depth Anything (~400MB)
- YOLOv8 nano (~6MB)
- OWL-ViT (~600MB)

### Documentation API

Documentation interactive Swagger : http://127.0.0.1:8000/docs

## 🎨 Captures d'écran

_(À venir : Screenshots de l'interface et des depth maps)_

## 📊 Progression du Projet

- ✅ **Sprint 1** : Fondations & Infrastructure (100%)
- ✅ **Sprint 2** : Vision & 3D - Depth Estimation (100%)
- ✅ **Sprint 3** : Intelligence Contractuelle (100%)
- 🔄 **Sprint 4** : UI/UX Premium & Finalisation (50%)

**Progression totale : ~88%**

Voir [SPRINTS.md](./SPRINTS.md) pour plus de détails.

## 📖 Documentation

- [Architecture](./ARCHITECTURE.md) - Détails techniques et choix d'architecture
- [Sprints](./SPRINTS.md) - Planification et roadmap du projet
- [Setup](./SETUP.md) - Guide d'installation détaillé

## 🎯 Pourquoi ce projet ?

Ce projet démontre des compétences avancées en :

- **Full-Stack Development** : Vue.js + Python/FastAPI
- **Intelligence Artificielle** : Intégration de modèles Hugging Face
- **Computer Vision** : Depth Estimation (top 1% des développeurs)
- **UX/UI moderne** : Design premium avec Tailwind
- **Architecture propre** : Services, API REST, gestion d'état

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

## 📝 License

MIT License - voir [LICENSE](./LICENSE)

---

**Développé par** [@machichiotte](https://github.com/machichiotte) | **2025**
