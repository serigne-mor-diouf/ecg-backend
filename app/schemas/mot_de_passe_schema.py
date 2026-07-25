from pydantic import BaseModel, EmailStr


class ChangerMotDePasseRequest(BaseModel):
    ancien_mot_de_passe: str
    nouveau_mot_de_passe: str


class MotDePasseOublieRequest(BaseModel):
    email: EmailStr


class ReinitialiserMotDePasseRequest(BaseModel):
    code: str
    nouveau_mot_de_passe: str
