from sqlalchemy.orm import Session

from app.models.administrateur import Administrateur
from app.models.medecin import Medecin
from app.models.utilisateur import Utilisateur


def get_by_email(db: Session, email: str) -> Utilisateur | None:
    return db.query(Utilisateur).filter(Utilisateur.email == email).first()


def get_by_id(db: Session, utilisateur_id: int) -> Utilisateur | None:
    return db.query(Utilisateur).filter(Utilisateur.id == utilisateur_id).first()


def create_medecin(db: Session, *, nom: str, prenom: str, email: str,
                    mot_de_passe_hash: str, specialite: str | None, numero_ordre: str) -> Medecin:
    medecin = Medecin(
        nom=nom, prenom=prenom, email=email,
        mot_de_passe_hash=mot_de_passe_hash, role="medecin",
        specialite=specialite, numero_ordre=numero_ordre,
    )
    db.add(medecin)
    db.commit()
    db.refresh(medecin)
    return medecin


def create_administrateur(db: Session, *, nom: str, prenom: str, email: str,
                           mot_de_passe_hash: str) -> Administrateur:
    admin = Administrateur(
        nom=nom, prenom=prenom, email=email,
        mot_de_passe_hash=mot_de_passe_hash, role="administrateur",
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin
