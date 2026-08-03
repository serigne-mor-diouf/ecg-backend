from pydantic import BaseModel

class PatientCreate(BaseModel):
    nom: str
    prenom: str
    age: int
    sexe: str
    antecedents: str | None = None
    adresse: str | None = None
    telephone: str | None = None

class PatientResponse(PatientCreate):
    id: int
    fichier_joint: str | None = None

    class Config:
        from_attributes = True   # permet de convertir un objet SQLAlchemy en réponse JSON
