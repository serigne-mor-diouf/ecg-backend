from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core.mail import envoyer_code_reinitialisation
from app.core.security import (
    creer_access_token,
    decoder_access_token,
    generer_code_validation,
    hash_password,
    verifier_mot_de_passe,
)
from app.models.utilisateur import Utilisateur
from app.repositories import token_repository, utilisateur_repository
from app.schemas.utilisateur_schema import AdministrateurCreate, MedecinCreate

DUREE_VALIDITE_RESET_MINUTES = 30


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
    if not utilisateur.actif:
        raise ValueError("Ce compte a été verrouillé, contactez un administrateur")
    return utilisateur


def generer_token(utilisateur: Utilisateur) -> str:
    return creer_access_token(sub=str(utilisateur.id), role=utilisateur.role)


def deconnecter(db: Session, token: str) -> None:
    payload = decoder_access_token(token)
    expire_at = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
    token_repository.revoquer(db, payload["jti"], expire_at)


def changer_mot_de_passe(db: Session, utilisateur: Utilisateur, ancien_mot_de_passe: str, nouveau_mot_de_passe: str) -> None:
    if not verifier_mot_de_passe(ancien_mot_de_passe, utilisateur.mot_de_passe_hash):
        raise ValueError("Ancien mot de passe incorrect")
    utilisateur_repository.set_mot_de_passe(db, utilisateur, hash_password(nouveau_mot_de_passe))


def demander_reinitialisation(db: Session, email: str) -> None:
    """Génère un code de validation à 6 chiffres et l'envoie par email.

    Lève une ValueError si l'email n'existe pas, pour retourner un message
    explicite à l'utilisateur (choix produit assumé ici, au prix de révéler
    quels emails sont enregistrés).
    """
    utilisateur = utilisateur_repository.get_by_email(db, email)
    if not utilisateur:
        raise ValueError("Aucun compte n'est associé à cet email")
    code = generer_code_validation()
    expire_at = datetime.now(timezone.utc) + timedelta(minutes=DUREE_VALIDITE_RESET_MINUTES)
    utilisateur_repository.set_reset_token(db, utilisateur, code, expire_at)
    envoyer_code_reinitialisation(utilisateur.email, code)


def reinitialiser_mot_de_passe(db: Session, code: str, nouveau_mot_de_passe: str) -> None:
    utilisateur = utilisateur_repository.get_by_reset_token(db, code)
    if not utilisateur or not utilisateur.reset_token_expire:
        raise ValueError("Code de validation invalide")
    if utilisateur.reset_token_expire < datetime.now(timezone.utc):
        raise ValueError("Code de validation expiré")
    utilisateur_repository.set_mot_de_passe(db, utilisateur, hash_password(nouveau_mot_de_passe))


def verrouiller_compte(db: Session, utilisateur_id: int) -> Utilisateur:
    utilisateur = utilisateur_repository.get_by_id(db, utilisateur_id)
    if not utilisateur:
        raise ValueError("Utilisateur introuvable")
    utilisateur_repository.set_actif(db, utilisateur, False)
    return utilisateur


def deverrouiller_compte(db: Session, utilisateur_id: int) -> Utilisateur:
    utilisateur = utilisateur_repository.get_by_id(db, utilisateur_id)
    if not utilisateur:
        raise ValueError("Utilisateur introuvable")
    utilisateur_repository.set_actif(db, utilisateur, True)
    return utilisateur
