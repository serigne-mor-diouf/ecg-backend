from pydantic import BaseModel, EmailStr


class UtilisateurBase(BaseModel):
    nom: str
    prenom: str
    email: EmailStr


class UtilisateurCreate(UtilisateurBase):
    mot_de_passe: str


class UtilisateurResponse(UtilisateurBase):
    id: int
    role: str
    actif: bool

    class Config:
        from_attributes = True


class MedecinCreate(UtilisateurCreate):
    specialite: str | None = None
    numero_ordre: str


class MedecinResponse(UtilisateurResponse):
    specialite: str | None = None
    numero_ordre: str


class AdministrateurCreate(UtilisateurCreate):
    pass


class AdministrateurResponse(UtilisateurResponse):
    pass
