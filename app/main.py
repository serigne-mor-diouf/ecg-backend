from fastapi import FastAPI
from app.routers import auth, patients
from app.database import Base, engine
from app.models import patients as patients_model   # importer le modèle pour qu'il soit enregistré dans Base
from app.models import utilisateur as utilisateur_model
from app.models import medecin as medecin_model
from app.models import administrateur as administrateur_model
from app.core.startup import creer_admin_par_defaut_si_absent

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Système intelligent d'interprétation ECG",
    description="Backend d'aide au diagnostic ECG assisté par IA",
    version="0.1.0",
)


@app.on_event("startup")
def seed_admin():
    creer_admin_par_defaut_si_absent()


app.include_router(auth.router)
app.include_router(patients.router)
