# Planification des Sprints - DamageControl AI

Ce document détaille la roadmap pour passer de l'idée au MVP (Minimum Viable Product) "CV-Ready".

## 🗓️ Vue d'ensemble

- **Sprint 1 : Fondations & Infrastructure** ✅ **TERMINÉ**
- **Sprint 2 : Vision & 3D** ✅ **TERMINÉ**
- **Sprint 3 : Intelligence Contractuelle & Backend** ✅ **TERMINÉ**
- **Sprint 4 : UI/UX Premium & Finalisation** 🔄 **PARTIEL (33%)**

---

## 🏃 Sprint 1 : Fondations & Infrastructure ✅

**Objectif :** Avoir une stack qui tourne (Frontend + Backend + Stockage) et une pipeline de déploiement locale.

### Tâches :

1.  **Setup Environnement :** ✅
    - [x] Initialiser le repo Git
    - [x] Pusher sur GitHub (https://github.com/machichiotte/damage-control-ai)
    - [x] Configurer le stockage local (pas de Docker pour le MVP)
2.  **Backend Skeleton (FastAPI) :** ✅
    - [x] Créer une route `POST /upload` qui reçoit une image et la stocke localement
    - [x] Créer une route `GET /health` pour vérifier que tout tourne
    - [x] Configuration CORS pour le frontend
3.  **Frontend Skeleton (Vue.js) :** ✅
    - [x] Initialiser Vue 3 avec Vite et TailwindCSS
    - [x] Créer une page d'accueil avec design moderne
    - [x] Créer un composant d'upload interactif avec drag & drop
    - [x] Connecter l'upload au backend
    - [x] Tester : Upload fonctionnel

**Résultat :** Stack complète opérationnelle avec upload d'images fonctionnel et interface premium.

---

## 🏃 Sprint 2 : Vision & 3D ✅

**Objectif :** Implémenter l'analyse d'image et la visualisation 3D. C'est le cœur de la démo.

### Tâches :

1.  **Service IA - Depth Estimation :** ✅
    - [x] Intégrer le modèle **Depth Anything** (Hugging Face)
    - [x] Créer un service `DepthEstimator` qui génère des depth maps
    - [x] Appliquer une colormap (INFERNO) pour visualisation
    - [x] Sauvegarder les depth maps générées
2.  **Backend - Endpoint d'analyse :** ✅
    - [x] Créer l'endpoint `POST /analyze/{filename}`
    - [x] Servir les fichiers statiques (images + depth maps)
    - [x] Gérer les erreurs et logging détaillé
3.  **Frontend - Visualisation :** ✅
    - [x] Ajouter un bouton "Analyser la profondeur (3D)"
    - [x] Afficher la comparaison côte à côte (original vs depth map)
    - [x] Afficher les statistiques de profondeur (min/max/mean)
    - [x] Animations de chargement pendant l'analyse
4.  **Tests & Debug :** ✅
    - [x] Résoudre les problèmes de compatibilité OpenCV
    - [x] Tester avec différentes images
    - [x] Valider que les depth maps sont correctes

**Résultat :** Analyse de profondeur 3D fonctionnelle avec visualisation impressionnante.

---

## 🏃 Sprint 3 : Intelligence Contractuelle & Backend ✅

**Objectif :** Donner du sens aux données visuelles en les croisant avec les contrats.

### Tâches :

1.  **Service IA - Object Detection (YOLO) :** ✅
    - [x] Intégrer YOLO pour détecter les objets/pièces dans l'image
    - [x] Identifier les pièces de voiture (Zero-Shot avec OWL-ViT)
    - [x] Afficher les bounding boxes sur l'image
2.  **Service IA - Analyse de Contrat :** ✅
    - [x] Créer un endpoint `POST /upload/contract` pour uploader un PDF/Image de contrat
    - [x] Implémenter l'extraction de texte (PyPDF2 + Tesseract OCR)
    - [x] Créer le service `ContractAnalyzer` avec analyse par regex
    - [x] Détecter franchise, plafond et types de garanties
    - [x] Créer l'endpoint `POST /analyze/contract/{filename}`
    - [x] Interface frontend `ContractUploader.vue` avec drag & drop
    - [x] Affichage des résultats (franchise, plafond, garanties)
3.  **Logique Métier :**
    - [ ] Créer un algorithme simple : `Estimation Dégât (Volume 3D) * Coût Pièce > Franchise ?`
    - [ ] Générer un JSON de résultat "Sinistre Couvert : OUI/NON"
    - [ ] Calculer une estimation de coût

**Résultat :** Application capable d'extraire et analyser les contrats d'assurance (PDF/Images). Reste à croiser avec l'analyse visuelle.

---

## 🏃 Sprint 4 : UI/UX Premium & Finalisation 🔄

**Objectif :** Rendre l'application belle et utilisable pour le portfolio.

### Tâches :

1.  **UI Design :**
    - [x] Appliquer un thème "Dark Mode" futuriste (Glassmorphism)
    - [x] Ajouter des animations de chargement pendant le traitement IA
    - [x] Système d'onglets pour navigation (Image / Contrat)
    - [ ] Créer une galerie des analyses précédentes
2.  **Visualisation 3D Interactive (TresJS) :** ✅
    - [x] Intégrer TresJS pour afficher la depth map en 3D
    - [x] Permettre la rotation et le zoom de la scène
    - [x] Ajouter la rotation automatique
    - [x] Displacement mapping pour relief 3D réel
3.  **PWA Features :**
    - [ ] Configurer le manifest pour que l'app soit installable sur mobile
    - [ ] Tester l'accès caméra sur mobile
    - [ ] Optimiser les performances
4.  **Documentation & Démo :**
    - [ ] Enregistrer une vidéo démo du flux complet
    - [ ] Finaliser le README avec des screenshots
    - [ ] Créer un CHANGELOG.md
    - [ ] Préparer une présentation portfolio

**Résultat partiel :** Visualisation 3D interactive fonctionnelle ! Reste UI polish et PWA.

---

## 📊 Progression Globale

- ✅ **Sprint 1** : 100% (3/3 tâches principales)
- ✅ **Sprint 2** : 100% (4/4 tâches principales)
- ✅ **Sprint 3** : 67% (2/3 tâches principales) - **Analyse de contrat terminée !**
- 🔄 **Sprint 4** : 50% (2/4 tâches principales - 3D visualization + UI design done)

**Progression totale : ~79% (3.17/4 sprints)**

---

## 🎯 Prochaines étapes recommandées

1. **Sprint 3 - Logique Métier** : Croiser analyse visuelle et contractuelle pour décision de couverture
2. **Sprint 4 - PWA** : Rendre l'app installable sur mobile
3. **Déploiement** : Déployer l'application en ligne (Vercel + Railway)

Le projet a déjà une base solide et impressionnante pour un portfolio !
