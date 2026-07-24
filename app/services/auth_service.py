from sqlalchemy.orm import Session

from app.core.security import creer_access_token, hash_password, verifier_mot_de_passe
from app.models.utilisateur import Utilisateur
from app.repositories import utilisateur_repository
from app.schemas.utilisateur_schema import AdministrateurCreate, MedecinCreate


def inscrire_medecin(db: Session, data: MedecinCreate):
    if utilisateur_repository.get_by_email(db, data.email):
        raise ValueError("Un compte existe déjà avec cet email")
    return utilisateur_repository.create_medecin(
        db,
        nom=data.nom, prenom=data.prenom, email=data.email,
        mot_de_passe_hash=hash_password(data.mot_de_passe),
        specialite=data.specialite, numero_ordre=data.numero_ordre,
    )


def inscrire_administrateur(db: Session, data: AdministrateurCreate):
    if utilisateur_repository.get_by_email(db, data.email):
        raise ValueError("Un compte existe déjà avec cet email")
    return utilisateur_repository.create_administrateur(
        db,
        nom=data.nom, prenom=data.prenom, email=data.email,
        mot_de_passe_hash=hash_password(data.mot_de_passe),
    )


def authentifier(db: Session, email: str, mot_de_passe: str) -> Utilisateur:
    utilisateur = utilisateur_repository.get_by_email(db, email)
    if not utilisateur or not verifier_mot_de_passe(mot_de_passe, utilisateur.mot_de_passe_hash):
        raise ValueError("Email ou mot de passe incorrect")
    return utilisateur


def generer_token(utilisateur: Utilisateur) -> str:
    return creer_access_token(sub=str(utilisateur.id), role=utilisateur.role)
