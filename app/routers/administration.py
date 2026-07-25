from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_administrateur
from app.database import get_db
from app.models.utilisateur import Utilisateur
from app.schemas.utilisateur_schema import UtilisateurResponse
from app.services import auth_service

router = APIRouter(prefix="/administration", tags=["Administration"])


@router.patch("/utilisateurs/{utilisateur_id}/verrouiller", response_model=UtilisateurResponse)
def verrouiller_compte(
    utilisateur_id: int,
    db: Session = Depends(get_db),
    _: Utilisateur = Depends(get_current_administrateur),
):
    try:
        return auth_service.verrouiller_compte(db, utilisateur_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/utilisateurs/{utilisateur_id}/deverrouiller", response_model=UtilisateurResponse)
def deverrouiller_compte(
    utilisateur_id: int,
    db: Session = Depends(get_db),
    _: Utilisateur = Depends(get_current_administrateur),
):
    try:
        return auth_service.deverrouiller_compte(db, utilisateur_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
