# Architecture Technique - DamageControl AI

## 🏗 Vue Globale

L'application suit une architecture micro-services simplifiée, conteneurisée avec Docker.

```mermaid
graph TD
    User[Utilisateur Mobile] -->|HTTPS| Frontend[Frontend Vue.js (PWA)]
    Frontend -->|API REST| Backend[Backend FastAPI]
    Backend -->|Stockage Images| MinIO[MinIO (S3 Compatible)]
    Backend -->|Inférence| AI_Models[Modèles Hugging Face]
    AI_Models -->|Depth Map| Backend
    AI_Models -->|Extraction Données| Backend
```

## 🔧 Choix Technologiques & Justification

### 1. Frontend : Vue.js 3 + TresJS

- **Pourquoi ?** Vous avez de l'expérience avec Vue.js. React était suggéré, mais Vue.js est tout aussi puissant pour ce cas d'usage.
- **3D :** Nous utiliserons **TresJS**, qui est l'équivalent de React-Three-Fiber mais pour l'écosystème Vue. Cela permet d'utiliser Three.js de manière déclarative (comme des composants HTML).
- **UI :** TailwindCSS pour un design rapide et moderne.

### 2. Backend : Python FastAPI

- **Pourquoi ?** C'est le standard de l'industrie pour servir des modèles IA. Rapide (Asynchrone) et documentation automatique (Swagger UI).
- **Traitement Image :** OpenCV et PIL pour manipuler les images avant l'envoi aux modèles.

### 3. Intelligence Artificielle (Hugging Face)

Nous utiliserons l'API `transformers` de Hugging Face pour charger les modèles localement ou via API (selon la puissance de votre machine).

- **Depth Estimation :** `LiheYoung/depth-anything-small-hf` (Léger et performant).
- **Table QA :** `google/tapas-base-finetuned-wtq` (Pour lire les tableaux).

### 4. Stockage : MinIO

- **Pourquoi ?** Vous vouliez une solution gratuite. MinIO est un serveur S3 open-source que l'on peut héberger soi-même via Docker.
- **Avantage :** Si un jour vous voulez passer en prod sur AWS S3 ou Google Cloud Storage, vous n'aurez **aucune ligne de code à changer**, juste la configuration.

## 📦 Structure des Données (MinIO)

- Bucket `raw-images` : Photos originales uploadées.
- Bucket `processed` : Depth maps, masques de segmentation, JSONs de résultats.
