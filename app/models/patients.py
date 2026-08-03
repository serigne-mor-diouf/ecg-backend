from sqlalchemy import Column, Integer, String
from app.database import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String)
    prenom = Column(String)
    age = Column(Integer)
    sexe = Column(String)
    antecedents = Column(String, nullable=True)
    adresse = Column(String, nullable=True)
    telephone = Column(String, nullable=True)
    fichier_joint = Column(String, nullable=True)  # chemin du document médical attaché (optionnel)