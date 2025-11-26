# Planification des Sprints - DamageControl AI

Ce document détaille la roadmap pour passer de l'idée au MVP (Minimum Viable Product) "CV-Ready".

## 🗓️ Vue d'ensemble

- **Sprint 1 : Fondations & Infrastructure**
- **Sprint 2 : Vision & 3D**
- **Sprint 3 : Intelligence Contractuelle & Backend**
- **Sprint 4 : Intégration & Polish**

---

## 🏃 Sprint 1 : Fondations & Infrastructure

**Objectif :** Avoir une stack qui tourne (Frontend + Backend + Stockage) et une pipeline de déploiement locale.

### Tâches :

1.  **Setup Environnement :**
    - [ ] Initialiser le repo Git.
    - [ ] Créer le `docker-compose.yml` avec FastAPI, MinIO (S3 local), et un service Frontend vide.
    - [ ] Configurer MinIO (Buckets `uploads`, `processed`).
2.  **Backend Skeleton (FastAPI) :**
    - [ ] Créer une route `POST /upload` qui reçoit une image et la stocke dans MinIO.
    - [ ] Créer une route `GET /health` pour vérifier que tout tourne.
3.  **Frontend Skeleton (Vue.js) :**
    - [ ] Initialiser Vue 3 avec Vite et TailwindCSS (pour le style rapide et premium).
    - [ ] Créer une page d'accueil simple avec un bouton d'upload (Camera capture).
    - [ ] Connecter l'upload au backend.

---

## 🏃 Sprint 2 : Vision & 3D (Le "Wow" Factor)

**Objectif :** Implémenter l'analyse d'image et la visualisation 3D. C'est le cœur de la démo.

### Tâches :

1.  **Service IA - Depth Estimation :**
    - [ ] Intégrer le modèle **Depth Anything** (Hugging Face) dans le backend.
    - [ ] Créer un worker qui prend une image, génère la depth map, et la sauve.
2.  **Visualisation 3D (TresJS) :**
    - [ ] Dans Vue.js, installer TresJS (Three.js pour Vue).
    - [ ] Créer un composant `DepthViewer.vue` qui prend l'image originale et la depth map pour créer un effet de relief interactif.
3.  **Service IA - Object Detection & Segmentation :**
    - [ ] Intégrer **YOLO** pour détecter les pièces (pare-chocs, portière).
    - [ ] (Optionnel pour MVP) Intégrer la segmentation pour détourer les dégâts.

---

## 🏃 Sprint 3 : Intelligence Contractuelle & Logique Métier

**Objectif :** Donner du sens aux données visuelles en les croisant avec les contrats.

### Tâches :

1.  **Service IA - Table QA (TAPAS) :**
    - [ ] Créer un endpoint pour uploader un PDF/Image de contrat.
    - [ ] Implémenter l'extraction de données (Franchise, Plafond) via TAPAS ou LayoutLM.
2.  **Logique Métier :**
    - [ ] Créer un algorithme simple : `Estimation Dégât (Volume 3D) * Coût Pièce > Franchise ?`.
    - [ ] Générer un JSON de résultat "Sinistre Couvert : OUI/NON".

---

## 🏃 Sprint 4 : UI/UX Premium & Finalisation

**Objectif :** Rendre l'application belle et utilisable pour le portfolio.

### Tâches :

1.  **UI Design :**
    - [ ] Appliquer un thème "Dark Mode" futuriste (Glassmorphism).
    - [ ] Ajouter des animations de chargement pendant le traitement IA (très important pour l'attente).
2.  **PWA Features :**
    - [ ] Configurer le manifest pour que l'app soit installable sur mobile.
    - [ ] Tester l'accès caméra sur mobile.
3.  **Documentation & Démo :**
    - [ ] Enregistrer une vidéo démo du flux complet.
    - [ ] Finaliser le README avec des screenshots.
