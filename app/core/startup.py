from app.core.config import settings
from app.core.security import hash_password
from app.database import SessionLocal
from app.repositories import utilisateur_repository


def creer_admin_par_defaut_si_absent() -> None:
    """Garantit qu'au moins un compte administrateur existe.

    Sans ce bootstrap, personne ne pourrait jamais appeler
    POST /auth/register/administrateur (réservé aux admins) ni créer
    de compte médecin par ce biais.
    """
    db = SessionLocal()
    try:
        admin_existe = db.query(utilisateur_repository.Administrateur).first()
        if admin_existe:
            return
        utilisateur_repository.create_administrateur(
            db,
            nom=settings.default_admin_nom,
            prenom=settings.default_admin_prenom,
            email=settings.default_admin_email,
            mot_de_passe_hash=hash_password(settings.default_admin_password),
        )
        print(f"[startup] Compte administrateur par défaut créé : {settings.default_admin_email}")
    finally:
        db.close()
