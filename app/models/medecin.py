from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.utilisateur import Utilisateur


class Medecin(Utilisateur):
    __tablename__ = "medecins"

    id = Column(Integer, ForeignKey("utilisateurs.id"), primary_key=True)
    specialite = Column(String, nullable=True)
    numero_ordre = Column(String, unique=True, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "medecin",
    }
