# Utiliser une image Python officielle légère
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système
# libgl1 : nécessaire pour OpenCV (cv2) - remplace libgl1-mesa-glx dans Debian Trixie
# tesseract-ocr : nécessaire pour l'analyse de contrats
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    tesseract-ocr \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier le fichier des dépendances Python
COPY requirements.txt .

# Installer les dépendances Python
# --no-cache-dir permet de garder l'image légère
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Créer un utilisateur non-root (Obligatoire pour Hugging Face Spaces)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Définir le répertoire de travail de l'utilisateur
WORKDIR $HOME/app

# Copier tout le code backend dans le conteneur
COPY --chown=user . $HOME/app

# Créer le dossier uploads
RUN mkdir -p $HOME/app/uploads

# Exposer le port 7860 (port par défaut de Hugging Face Spaces)
EXPOSE 7860

# Commande de démarrage
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
