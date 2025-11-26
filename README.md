# DamageControl AI - L'Expert en Sinistres Automatisé

## 🎯 Concept

DamageControl AI est une Progressive Web App (PWA) révolutionnaire qui automatise l'évaluation des dommages automobiles et domestiques. En utilisant l'intelligence artificielle pour l'analyse d'images (profondeur, segmentation, détection) et le traitement du langage naturel (analyse de contrats), elle accélère le processus de déclaration de sinistre (FNOL) et réduit la fraude.

## 🚀 Fonctionnalités Clés

1.  **Depth Estimation (Vision 3D)** : Analyse de la gravité des impacts via des cartes de profondeur.
2.  **Segmentation & Détection** : Identification précise des pièces endommagées et de la surface à réparer.
3.  **Analyse de Contrat (NLP)** : Extraction automatique des franchises et garanties depuis des PDF.
4.  **Rapport Automatisé** : Croisement des données visuelles et contractuelles pour une estimation immédiate.

## 🛠 Stack Technique

- **Frontend** : Vue.js 3 (Vite) + TresJS (Three.js pour Vue) + TailwindCSS
- **Backend** : Python (FastAPI)
- **IA/ML** : Hugging Face (Depth Anything, SegFormer, YOLO, TAPAS)
- **Stockage** : Local (fichiers) pour le développement

## 📂 Structure du Projet

```
/damage_control_ai
├── /frontend          # Application Vue.js
├── /backend           # API FastAPI
└── /docs              # Documentation et Planification
```

## 🏁 Démarrage Rapide

### Prérequis

- Node.js 18+
- Python 3.9+

### Installation

**Frontend :**

```bash
cd frontend
npm install
npm run dev
```

Le frontend sera accessible sur http://localhost:5173

**Backend :**

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Le backend sera accessible sur http://127.0.0.1:8000

### Documentation API

Une fois le backend lancé, accédez à la documentation interactive Swagger : http://127.0.0.1:8000/docs

## 📖 Documentation

- [Architecture](./ARCHITECTURE.md) - Détails techniques et choix d'architecture
- [Sprints](./SPRINTS.md) - Planification et roadmap du projet
- [Setup](./SETUP.md) - Guide d'installation détaillé

## 📝 License

MIT License - voir [LICENSE](./LICENSE)
