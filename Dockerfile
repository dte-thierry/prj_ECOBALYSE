# Utiliser l'image Python 3.9 slim comme base
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de requirements et le script Python dans le conteneur
COPY requirements.txt .
COPY ecobalyse_generator.py .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Créer un répertoire pour les données de sortie
RUN mkdir /data

# Définir le volume pour les données de sortie
VOLUME /data

# Exécuter le script quand le conteneur démarre
CMD ["python", "ecobalyse_generator.py"]