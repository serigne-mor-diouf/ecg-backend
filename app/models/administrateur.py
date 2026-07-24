from sqlalchemy import Column, Integer, ForeignKey
from app.models.utilisateur import Utilisateur


class Administrateur(Utilisateur):
    __tablename__ = "administrateurs"

    id = Column(Integer, ForeignKey("utilisateurs.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "administrateur",
    }
