"""Crée le tout premier compte administrateur (bootstrap).

Usage:
    venv/Scripts/python.exe scripts/seed_admin.py <email> <mot_de_passe> <nom> <prenom>
"""
import sys

sys.path.append(".")

from app.database import SessionLocal
from app.repositories import utilisateur_repository
from app.core.security import hash_password


def main():
    if len(sys.argv) != 5:
        print("Usage: seed_admin.py <email> <mot_de_passe> <nom> <prenom>")
        sys.exit(1)

    email, mot_de_passe, nom, prenom = sys.argv[1:5]
    db = SessionLocal()
    try:
        if utilisateur_repository.get_by_email(db, email):
            print(f"Un compte existe déjà pour {email}")
            return
        admin = utilisateur_repository.create_administrateur(
            db, nom=nom, prenom=prenom, email=email,
            mot_de_passe_hash=hash_password(mot_de_passe),
        )
        print(f"Administrateur créé : id={admin.id}, email={admin.email}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
