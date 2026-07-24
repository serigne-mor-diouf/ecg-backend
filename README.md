# ECG Backend

API backend (FastAPI) pour un système intelligent d'aide au diagnostic ECG.

## Sommaire

- [Stack technique](#stack-technique)
- [Architecture](#architecture)
- [Démarrage rapide](#démarrage-rapide)
- [Compte administrateur par défaut](#compte-administrateur-par-défaut)
- [Authentification](#authentification)
- [Fichiers stratégiques](#fichiers-stratégiques)
- [Commandes utiles](#commandes-utiles)

---

## Stack technique

- **FastAPI** — framework web
- **SQLAlchemy** — ORM
- **PostgreSQL** (via `psycopg2`) — base de données
- **Pydantic / pydantic-settings** — validation des données et configuration
- **PyJWT** + **bcrypt** — authentification par token JWT et hash des mots de passe
- **Uvicorn** — serveur ASGI

## Architecture

Le projet suit une architecture en couches, avec séparation stricte des responsabilités. Chaque couche ne connaît que la couche immédiatement en dessous (principe : fermé à la modification, ouvert à l'extension — on ajoute des fonctionnalités sans casser l'existant).

```
app/
├── main.py                    # point d'entrée FastAPI : montage des routers, création des tables, seed admin
├── core/
│   ├── config.py               # Settings (pydantic-settings) — lit le .env
│   ├── security.py             # hash bcrypt, génération/décodage JWT
│   ├── dependencies.py         # get_current_user, require_role(...) — protection des routes
│   └── startup.py              # création du compte admin par défaut au démarrage
├── database.py                 # engine SQLAlchemy, SessionLocal, get_db(), Base
├── models/                     # entités SQLAlchemy (tables réelles)
│   ├── utilisateur.py          # classe mère (héritage par jointure)
│   ├── medecin.py               # hérite de Utilisateur
│   ├── administrateur.py       # hérite de Utilisateur
│   └── patients.py
├── schemas/                    # schémas Pydantic (validation entrée/sortie API)
│   ├── utilisateur_schema.py
│   ├── token_schema.py
│   └── patient_schema.py
├── repositories/                # accès données brut (requêtes SQLAlchemy, aucune logique métier)
│   ├── utilisateur_repository.py
│   └── patient_repository.py
├── services/                    # logique métier, orchestration, règles de gestion
│   ├── auth_service.py
│   └── patient_service.py
└── routers/                     # endpoints FastAPI (appellent uniquement les services)
    ├── auth.py
    ├── patients.py
    └── ecg.py
```

**Règle à respecter en ajoutant du code :**
- Un `router` n'appelle jamais SQLAlchemy directement : il passe par un `service`.
- Un `service` ne connaît jamais la session HTTP/FastAPI : il reçoit une `Session` SQLAlchemy et des schémas Pydantic.
- Un `repository` ne contient aucune règle métier : uniquement des requêtes.
- Un `model` (SQLAlchemy) ≠ un `schema` (Pydantic) : ne jamais les confondre.

### Hiérarchie des utilisateurs

`Utilisateur` est la classe mère (table `utilisateurs`), avec héritage par jointure SQLAlchemy :
- `Medecin` (table `medecins`) — spécialité, numéro d'ordre.
- `Administrateur` (table `administrateurs`) — gère les comptes.

Le champ `type` (colonne polymorphique) permet à SQLAlchemy de retourner automatiquement le bon sous-type quand on interroge `Utilisateur`.

## Démarrage rapide

### 1. Prérequis

- Python 3.11+ installé
- PostgreSQL installé et démarré localement

### 2. Cloner et créer l'environnement virtuel

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

### 3. Configurer les variables d'environnement

Créer un fichier `.env` à la racine du projet (non versionné) :

```env
DATABASE_URL=postgresql://postgres:<mot_de_passe>@localhost:5432/ecg_db
JWT_SECRET_KEY=<clé secrète aléatoire longue>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DEFAULT_ADMIN_EMAIL=admin@ecg.com
DEFAULT_ADMIN_PASSWORD=Admin1234
DEFAULT_ADMIN_NOM=Admin
DEFAULT_ADMIN_PRENOM=Systeme
```

Générer une clé secrète JWT :
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

La base `ecg_db` doit exister sur le serveur PostgreSQL (`CREATE DATABASE ecg_db;` si besoin) — les **tables**, elles, sont créées automatiquement au démarrage de l'application.

### 4. Lancer l'application

```bash
venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

L'API est disponible sur http://127.0.0.1:8000, la documentation interactive sur http://127.0.0.1:8000/docs.

## Compte administrateur par défaut

**Au premier démarrage de l'application, si aucun compte administrateur n'existe en base, un compte admin est créé automatiquement** avec les identifiants définis dans `.env` (`DEFAULT_ADMIN_EMAIL` / `DEFAULT_ADMIN_PASSWORD`).

Avec les valeurs par défaut ci-dessus :
- **Email :** `admin@ecg.com`
- **Mot de passe :** `Admin1234`

⚠️ **À changer avant tout déploiement réel** — ce sont des identifiants de démo, à ne jamais garder en production. Modifier `DEFAULT_ADMIN_PASSWORD` dans `.env` avant le premier lancement sur un environnement partagé.

Cette création est **idempotente** : elle ne s'exécute que si aucun administrateur n'existe déjà, donc redémarrer l'app ne crée pas de doublons (voir `app/core/startup.py`).

## Authentification

Flow JWT simple (pas d'OAuth2 complet — pas besoin de `client_id`/`client_secret`) :

1. `POST /auth/login` avec un JSON `{"email": "...", "mot_de_passe": "..."}` → retourne un `access_token` + les infos de l'utilisateur connecté.
2. Envoyer ce token dans le header `Authorization: Bearer <token>` sur les routes protégées.
3. Dans Swagger (`/docs`) : cliquer sur **Authorize**, coller uniquement le token brut (sans le mot "Bearer").

Rôles et accès :
- `POST /auth/register/medecin` — public (inscription libre d'un médecin).
- `POST /auth/register/administrateur` — **protégé**, uniquement accessible par un administrateur déjà connecté.
- `GET /auth/me` — nécessite un token valide, retourne l'utilisateur courant.

## Fichiers stratégiques

| Fichier | Rôle |
|---|---|
| `app/main.py` | Point d'entrée : crée les tables, déclenche le seed admin, monte les routers |
| `app/core/config.py` | Source unique de vérité pour la configuration (lit `.env` via pydantic-settings) |
| `app/core/security.py` | Hash bcrypt des mots de passe, création/décodage des JWT |
| `app/core/dependencies.py` | `get_current_user`, `get_current_medecin`, `get_current_administrateur` — à utiliser via `Depends(...)` pour protéger une route |
| `app/core/startup.py` | Logique de création du compte admin par défaut |
| `app/database.py` | Connexion PostgreSQL (`engine`, `SessionLocal`, `get_db`) |
| `.env` | Secrets et configuration locale — **ne jamais committer** |
| `requirements.txt` | Dépendances exactes du projet (généré via `pip freeze`) |
| `scripts/seed_admin.py` | Création manuelle d'un compte admin (utile en complément du seed automatique) |

## Commandes utiles

```bash
# Lancer le serveur en mode développement (rechargement automatique)
venv\Scripts\python.exe -m uvicorn app.main:app --reload

# Créer un administrateur manuellement (en plus du seed automatique)
venv\Scripts\python.exe scripts/seed_admin.py <email> <mot_de_passe> <nom> <prenom>

# Installer une nouvelle dépendance puis figer requirements.txt
pip install <package>
pip freeze > requirements.txt
```
