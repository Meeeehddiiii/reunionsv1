# Utilisation de l'image officielle Python comme base
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers locaux dans le conteneur
COPY . /app

# Installer les dépendances de l'application
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port sur lequel l'application écoute (exemple: 5000)
EXPOSE 5000

# Commande pour démarrer l'application Python
CMD ["python", "app.py"]
