# Étape 1 : image officielle uv
FROM astral/uv:python3.12-bookworm-slim



# Étape 2 : variables d'environnement pour Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Étape 3 : dossier de travail dans le container
WORKDIR /app

# Étape 4 : copier pyproject 
COPY pyproject.toml .


# Install dependencies
RUN uv sync

# Étape 5 : copier le contenu du sous-dossier app
COPY . .

# Étape 6 : exposer le port Flask
EXPOSE 5000

# Étape 7 : commande pour démarrer l'application avec uv

CMD ["uv","run", "main.py"]


