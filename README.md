# MEV Form Application

Une application conteneurisée avec FastAPI backend, base de données MongoDB, et interface Streamlit.

| Composant       | Choix                       | Pourquoi                              |
| --------------- | --------------------------- | ------------------------------------- |
| Frontend        | python streamlite           | simple                                |
| Backend         | FastAPI                     | REST API pour stocker JSON            |
| Base de données | MongoDB                     | Pour persister formulaires & réponses |
| Déploiement     | Docker Compose              | Facilement portable et modifiable     |

## Architecture

- **Backend**: FastAPI avec fastapi-users pour l'authentification
- **Base de données**: MongoDB
- **Frontend**: Interface admin Streamlit

## Installation et Configuration

### Prérequis

- Docker et Docker Compose

### Configuration

1. Modifiez le fichier `.env` pour configurer votre application:
```
# Configuration MongoDB
MONGODB_URL=mongodb://mongodb:27017
MONGODB_DB=mev_form_db
MONGO_PORT=27017

# Configuration Backend
BACKEND_PORT=8000
JWT_SECRET=your_super_secret_key_change_this_in_production
JWT_LIFETIME_SECONDS=3600

# Configuration Frontend
FRONTEND_PORT=8501
API_URL=http://backend:8000

# Configuration Utilisateur Admin
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=adminpassword123
```

### Lancement de l'Application

Démarrez l'application avec Docker Compose:

```bash
docker-compose up -d
```

Cela lancera:
- Base de données MongoDB (avec logs minimisés)
- Backend FastAPI sur le port 8000
- Frontend Streamlit sur le port 8501

### Accès à l'Application

- **Frontend**: http://localhost:8501
- **API Backend**: http://localhost:8000
- **Documentation API**: http://localhost:8000/docs

## Premier Login

Un utilisateur admin est automatiquement créé lors du premier démarrage en utilisant les identifiants spécifiés dans le fichier `.env`:

- Email: (valeur de ADMIN_EMAIL dans .env)
- Mot de passe: (valeur de ADMIN_PASSWORD dans .env)

## Fonctionnalités

- **Authentification**: Login, logout, et gestion de session
- **Gestion des Utilisateurs**: Les admins peuvent créer de nouveaux utilisateurs
- **Interface Admin**: Tableau de bord admin sécurisé

## Développement

### Structure du Projet

```
mev-form/
├── .env                  # Variables d'environnement
├── backend/              # Backend FastAPI
│   ├── app/              # Code de l'application
│   ├── scripts/          # Scripts utilitaires
│   └── Dockerfile        # Définition du conteneur backend
├── docker-compose.yaml   # Configuration Docker Compose
└── frontend/             # Frontend Streamlit
    ├── app/              # Code de l'app Streamlit
    └── Dockerfile        # Définition du conteneur frontend
```
