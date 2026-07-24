from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    mot_de_passe: str


class UtilisateurConnecte(BaseModel):
    id: int
    nom: str
    prenom: str
    email: str
    role: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    utilisateur: UtilisateurConnecte
