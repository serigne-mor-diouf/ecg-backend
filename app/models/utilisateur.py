from sqlalchemy import Column, Integer, String
from app.database import Base


class Utilisateur(Base):
    """Classe mère de la hiérarchie (Utilisateur -> Medecin / Administrateur).

    Héritage par jointure : la table `utilisateurs` porte les champs communs,
    et `medecins` / `administrateurs` référencent `utilisateurs.id` en clé
    étrangère. La colonne `type` est le discriminant polymorphique.
    """

    __tablename__ = "utilisateurs"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    mot_de_passe_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)

    type = Column(String, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "utilisateur",
        "polymorphic_on": type,
    }
