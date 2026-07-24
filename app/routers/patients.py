from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import patient_service
from app.schemas.patient_schema import PatientCreate, PatientResponse

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.post("/", response_model=PatientResponse)
def creer_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    return patient_service.enregistrer_patient(db, patient)

@router.get("/", response_model=list[PatientResponse])
def lister_patients(db: Session = Depends(get_db)):
    return patient_service.obtenir_tous_les_patients(db)

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

@router.delete("/{patient_id}", status_code=204)
def supprimer_patient(patient_id: int, db: Session = Depends(get_db)):
    try:
        patient_service.supprimer_patient(db, patient_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))