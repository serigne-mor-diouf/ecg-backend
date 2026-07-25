import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import decoder_access_token
from app.database import get_db
from app.models.utilisateur import Utilisateur
from app.repositories import token_repository, utilisateur_repository

bearer_scheme = HTTPBearer()


def get_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> dict:
    erreur_auth = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Identifiants invalides",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decoder_access_token(credentials.credentials)
    except jwt.PyJWTError:
        raise erreur_auth

    if payload.get("sub") is None or payload.get("jti") is None:
        raise erreur_auth
    if token_repository.est_revoque(db, payload["jti"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ce token a été invalidé (déconnexion). Reconnectez-vous.",
        )
    return payload


def get_current_user(
    payload: dict = Depends(get_token_payload),
    db: Session = Depends(get_db),
) -> Utilisateur:
    utilisateur = utilisateur_repository.get_by_id(db, int(payload["sub"]))
    if utilisateur is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Identifiants invalides")
    if not utilisateur.actif:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Ce compte a été verrouillé")
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
