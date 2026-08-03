from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_medecin
from app.database import get_db
from app.services import patient_service
from app.core.storage import enregistrer_fichier_patient
from app.schemas.patient_schema import PatientCreate, PatientResponse

router = APIRouter(prefix="/patients", tags=["Patients"], dependencies=[Depends(get_current_medecin)])

@router.post("/", response_model=PatientResponse)
def creer_patient(
    nom: str = Form(...),
    prenom: str = Form(...),
    age: int = Form(...),
    sexe: str = Form(...),
    antecedents: str | None = Form(None),
    adresse: str | None = Form(None),
    telephone: str | None = Form(None),
    fichier: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    """Le fichier est optionnel : on peut le joindre dès la création du
    dossier, ou l'ajouter plus tard via PUT /patients/{id}/fichier."""
    patient_data = PatientCreate(
        nom=nom, prenom=prenom, age=age, sexe=sexe,
        antecedents=antecedents, adresse=adresse, telephone=telephone,
    )
    patient = patient_service.enregistrer_patient(db, patient_data)

    if fichier is not None and fichier.filename:
        contenu = fichier.file.read()
        try:
            chemin = enregistrer_fichier_patient(patient.id, fichier.filename, contenu)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        patient = patient_service.joindre_fichier(db, patient.id, chemin)

    return patient

@router.get("/", response_model=list[PatientResponse])
def lister_patients(db: Session = Depends(get_db)):
    return patient_service.obtenir_tous_les_patients(db)

@router.get("/recherche", response_model=list[PatientResponse])
def rechercher_patients(q: str, db: Session = Depends(get_db)):
    try:
        return patient_service.rechercher_patients(db, q)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{patient_id}", response_model=PatientResponse)
def lire_patient(patient_id: int, db: Session = Depends(get_db)):
    try:
        return patient_service.obtenir_patient(db, patient_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{patient_id}", response_model=PatientResponse)
def mettre_a_jour_patient(patient_id: int, patient: PatientCreate, db: Session = Depends(get_db)):
    try:
        return patient_service.modifier_patient(db, patient_id, patient)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{patient_id}/fichier", response_model=PatientResponse)
def joindre_fichier_patient(patient_id: int, fichier: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        patient_service.obtenir_patient(db, patient_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    contenu = fichier.file.read()
    try:
        chemin = enregistrer_fichier_patient(patient_id, fichier.filename, contenu)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return patient_service.joindre_fichier(db, patient_id, chemin)

@router.delete("/{patient_id}", status_code=204)
def supprimer_patient(patient_id: int, db: Session = Depends(get_db)):
    try:
        patient_service.supprimer_patient(db, patient_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
