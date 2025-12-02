# Guide de Déploiement Gratuit - DamageControl AI

Ce guide explique comment déployer **gratuitement** le projet complet (Frontend + Backend) sur Render.com et Netlify.

## 🎯 Architecture de Déploiement

- **Frontend** : Netlify (gratuit, illimité)
- **Backend** : Render.com (gratuit, 750h/mois, s'endort après 15min d'inactivité)

---

## 📦 Partie 1 : Déployer le Backend sur Render.com

### Étape 1 : Créer un compte Render

1. Aller sur [render.com](https://render.com)
2. S'inscrire avec GitHub (recommandé)
3. Autoriser Render à accéder à ton repo GitHub

### Étape 2 : Créer un nouveau Web Service

1. Cliquer sur **"New +"** → **"Web Service"**
2. Sélectionner le repo **`damage-control-ai`**
3. Configurer le service :

   **Settings :**

   - **Name** : `damage-control-ai-backend`
   - **Region** : `Frankfurt (EU Central)` (ou le plus proche)
   - **Branch** : `main`
   - **Root Directory** : `backend`
   - **Runtime** : `Python 3`
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. Sélectionner le **plan gratuit** (Free)

### Étape 3 : Configurer les Variables d'Environnement

Dans la section **Environment** de Render, ajouter :

```
FRONTEND_URL=https://ton-app.netlify.app
PYTHON_VERSION=3.9.18
```

⚠️ **Note** : Tu mettras à jour `FRONTEND_URL` après avoir déployé le frontend sur Netlify.

### Étape 4 : Déployer

1. Cliquer sur **"Create Web Service"**
2. Attendre le déploiement (~10-15 minutes pour télécharger les modèles IA)
3. Noter l'URL du backend : `https://damage-control-ai-backend.onrender.com`

⚠️ **Limitations du plan gratuit Render** :

- Le service s'endort après **15 minutes** d'inactivité
- Premier appel après sommeil : **~30 secondes** de démarrage
- **750 heures/mois** gratuites (suffisant pour un portfolio)

---

## 🌐 Partie 2 : Déployer le Frontend sur Netlify

### Étape 1 : Créer un compte Netlify

1. Aller sur [netlify.com](https://netlify.com)
2. S'inscrire avec GitHub
3. Autoriser Netlify à accéder à ton repo

### Étape 2 : Créer un nouveau site

1. Cliquer sur **"Add new site"** → **"Import an existing project"**
2. Sélectionner **GitHub**
3. Choisir le repo **`damage-control-ai`**

### Étape 3 : Configurer le build

**Build settings :**

- **Base directory** : `frontend`
- **Build command** : `npm run build`
- **Publish directory** : `frontend/dist`

### Étape 4 : Configurer les Variables d'Environnement

Dans **Site settings** → **Environment variables**, ajouter :

```
VITE_API_URL=https://damage-control-ai-backend.onrender.com
```

### Étape 5 : Déployer

1. Cliquer sur **"Deploy site"**
2. Attendre le build (~2-3 minutes)
3. Noter l'URL du frontend : `https://random-name-123.netlify.app`

### Étape 6 : Personnaliser le nom de domaine (optionnel)

1. Aller dans **Site settings** → **Domain management**
2. Cliquer sur **"Options"** → **"Edit site name"**
3. Choisir un nom : `damage-control-ai.netlify.app`

---

## 🔄 Partie 3 : Finaliser la Configuration

### 1. Mettre à jour le Backend avec l'URL du Frontend

Retourner sur **Render.com** :

1. Aller dans ton service backend
2. **Environment** → Modifier `FRONTEND_URL`
3. Mettre : `https://damage-control-ai.netlify.app`
4. Sauvegarder (le service va redémarrer)

### 2. Mettre à jour le Frontend avec l'URL du Backend

Dans ton code local, vérifier que `frontend/src/main.js` ou `frontend/src/config.js` utilise bien :

```javascript
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
```

Si ce n'est pas le cas, il faut mettre à jour le code pour utiliser la variable d'environnement.

---

## ✅ Vérification du Déploiement

### Tester le Backend

Ouvrir dans le navigateur :

```
https://damage-control-ai-backend.onrender.com/health
```

Tu devrais voir :

```json
{
  "status": "ok",
  "upload_dir": "/opt/render/project/src/uploads"
}
```

### Tester le Frontend

Ouvrir :

```
https://damage-control-ai.netlify.app
```

L'application devrait se charger et être fonctionnelle !

---

## 🚨 Problèmes Courants

### Backend : "Service Unavailable"

- **Cause** : Le service s'est endormi (inactif >15min)
- **Solution** : Attendre 30 secondes, il redémarre automatiquement

### Frontend : Erreur CORS

- **Cause** : `FRONTEND_URL` mal configurée sur Render
- **Solution** : Vérifier que l'URL est exacte (avec https://)

### Backend : Build échoue

- **Cause** : Modèles IA trop lourds (limite de RAM)
- **Solution** : Utiliser des modèles plus petits ou passer au plan payant

### Frontend : API non accessible

- **Cause** : `VITE_API_URL` mal configurée
- **Solution** : Vérifier dans Netlify → Environment variables

---

## 💰 Coûts

- **Netlify** : 100% gratuit (bande passante illimitée)
- **Render** : 100% gratuit (750h/mois)
- **Total** : **0€/mois** 🎉

---

## 🔄 Déploiement Automatique

Les deux services sont configurés pour **déployer automatiquement** à chaque push sur `main` :

1. Tu push sur GitHub
2. Netlify rebuild le frontend (~2min)
3. Render rebuild le backend (~10min)

---

## 📊 Monitoring

### Netlify

- Dashboard : https://app.netlify.com
- Voir les builds, logs, analytics

### Render

- Dashboard : https://dashboard.render.com
- Voir les logs en temps réel, métriques

---

## 🎯 Prochaines Étapes

1. ✅ Déployer le backend sur Render
2. ✅ Déployer le frontend sur Netlify
3. ✅ Configurer les variables d'environnement
4. 📸 Tester l'application en production
5. 📝 Mettre à jour le README avec les liens de démo
6. 🎥 Enregistrer une vidéo démo

---

**Bon déploiement ! 🚀**
