# Guide d'Installation & Démarrage

## Pré-requis

- Docker Desktop installé et lancé.
- Node.js (v18+) installé.
- Python (v3.9+) installé.

## 1. Initialisation du Projet

Le projet est divisé en deux dossiers principaux : `backend` et `frontend`.

### Backend

```bash
cd backend
python -m venv venv
# Windows
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

## 2. Lancer l'Infrastructure (MinIO)

Nous utilisons Docker pour le stockage S3 local.

```bash
docker-compose up -d minio
```

Accès console MinIO : http://localhost:9001 (User: `minioadmin`, Pass: `minioadmin`)

## 3. Lancer le Développement

### Backend

```bash
uvicorn main:app --reload
```

### Frontend

```bash
npm run dev
```

## 4. Structure des Dossiers

```
/damage_control_ai
├── docker-compose.yml  # Orchestration
├── /backend            # API Python
│   ├── main.py         # Point d'entrée
│   ├── /models         # Logique IA
│   └── /services       # S3, DB
└── /frontend           # Vue.js App
    ├── /src
    │   ├── /components # Composants Vue
    │   └── /tres       # Scènes 3D
```
