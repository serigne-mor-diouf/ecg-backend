from sqlalchemy.orm import Session
from app.models.patients import Patient
from app.schemas.patient_schema import PatientCreate

def create_patient(db: Session, patient: PatientCreate) -> Patient:
    db_patient = Patient(**patient.model_dump())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def get_patient_by_id(db: Session, patient_id: int) -> Patient | None:
    return db.query(Patient).filter(Patient.id == patient_id).first()

def get_all_patients(db: Session) -> list[Patient]:
    return db.query(Patient).all()

def rechercher_patients(db: Session, terme: str) -> list[Patient]:
    motif = f"%{terme}%"
    return db.query(Patient).filter(
        (Patient.nom.ilike(motif)) | (Patient.prenom.ilike(motif))
    ).all()

def set_fichier_joint(db: Session, patient: Patient, chemin_fichier: str) -> Patient:
    patient.fichier_joint = chemin_fichier
    db.commit()
    db.refresh(patient)
    return patient

def update_patient(db: Session, patient_id: int, patient: PatientCreate) -> Patient | None:
    db_patient = get_patient_by_id(db, patient_id)
    if not db_patient:
        return None
    for key, value in patient.model_dump().items():
        setattr(db_patient, key, value)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def delete_patient(db: Session, patient_id: int) -> bool:
    db_patient = get_patient_by_id(db, patient_id)
    if not db_patient:
        return False
    db.delete(db_patient)
    db.commit()
    return True