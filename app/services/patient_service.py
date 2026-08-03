from sqlalchemy.orm import Session
from app.repositories import patient_repository
from app.schemas.patient_schema import PatientCreate

def enregistrer_patient(db: Session, patient: PatientCreate):
    # ici on pourrait ajouter des règles métier
    # ex: vérifier l'âge, valider le sexe, logguer l'action...
    return patient_repository.create_patient(db, patient)

def obtenir_patient(db: Session, patient_id: int):
    patient = patient_repository.get_patient_by_id(db, patient_id)
    if not patient:
        raise ValueError("Patient introuvable")
    return patient

def obtenir_tous_les_patients(db: Session):
    return patient_repository.get_all_patients(db)

def rechercher_patients(db: Session, terme: str):
    if not terme or not terme.strip():
        raise ValueError("Le terme de recherche ne peut pas être vide")
    return patient_repository.rechercher_patients(db, terme.strip())

def modifier_patient(db: Session, patient_id: int, patient: PatientCreate):
    updated = patient_repository.update_patient(db, patient_id, patient)
    if not updated:
        raise ValueError("Patient introuvable")
    return updated 

def supprimer_patient(db: Session, patient_id: int):
    deleted = patient_repository.delete_patient(db, patient_id)
    if not deleted:
        raise ValueError("Patient introuvable")

def joindre_fichier(db: Session, patient_id: int, chemin_fichier: str):
    patient = patient_repository.get_patient_by_id(db, patient_id)
    if not patient:
        raise ValueError("Patient introuvable")
    return patient_repository.set_fichier_joint(db, patient, chemin_fichier)