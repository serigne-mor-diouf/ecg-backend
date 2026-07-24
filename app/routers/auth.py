from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_administrateur, get_current_user
from app.database import get_db
from app.models.utilisateur import Utilisateur
from app.schemas.token_schema import LoginRequest, Token
from app.schemas.utilisateur_schema import (
    AdministrateurCreate,
    AdministrateurResponse,
    MedecinCreate,
    MedecinResponse,
    UtilisateurResponse,
)
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Authentification"])


@router.post("/register/medecin", response_model=MedecinResponse, status_code=201)
def inscrire_medecin(data: MedecinCreate, db: Session = Depends(get_db)):
    try:
        return auth_service.inscrire_medecin(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/register/administrateur", response_model=AdministrateurResponse, status_code=201)
def inscrire_administrateur(
    data: AdministrateurCreate,
    db: Session = Depends(get_db),
    _: Utilisateur = Depends(get_current_administrateur),
):
    # seul un administrateur déjà authentifié peut créer un autre compte admin
    try:
        return auth_service.inscrire_administrateur(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=Token)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    try:
        utilisateur = auth_service.authentifier(db, data.email, data.mot_de_passe)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    token = auth_service.generer_token(utilisateur)
    return Token(access_token=token, utilisateur=utilisateur)


@router.get("/me", response_model=UtilisateurResponse)
def me(utilisateur: Utilisateur = Depends(get_current_user)):
    return utilisateur
