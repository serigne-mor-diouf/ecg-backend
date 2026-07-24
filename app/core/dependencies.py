import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import decoder_access_token
from app.database import get_db
from app.models.utilisateur import Utilisateur
from app.repositories import utilisateur_repository

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> Utilisateur:
    erreur_auth = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Identifiants invalides",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decoder_access_token(credentials.credentials)
        utilisateur_id = payload.get("sub")
        if utilisateur_id is None:
            raise erreur_auth
    except jwt.PyJWTError:
        raise erreur_auth

    utilisateur = utilisateur_repository.get_by_id(db, int(utilisateur_id))
    if utilisateur is None:
        raise erreur_auth
    return utilisateur


def require_role(role_attendu: str):
    def dependance(utilisateur: Utilisateur = Depends(get_current_user)) -> Utilisateur:
        if utilisateur.role != role_attendu:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Accès réservé au rôle '{role_attendu}'",
            )
        return utilisateur
    return dependance


get_current_medecin = require_role("medecin")
get_current_administrateur = require_role("administrateur")
