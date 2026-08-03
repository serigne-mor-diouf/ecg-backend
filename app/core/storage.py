import uuid
from pathlib import Path

DOSSIER_UPLOADS = Path("uploads/patients")
EXTENSIONS_AUTORISEES = {".pdf", ".jpg", ".jpeg", ".png"}
TAILLE_MAX_OCTETS = 10 * 1024 * 1024  # 10 Mo


def enregistrer_fichier_patient(patient_id: int, nom_original: str, contenu: bytes) -> str:
    extension = Path(nom_original).suffix.lower()
    if extension not in EXTENSIONS_AUTORISEES:
        raise ValueError(f"Type de fichier non autorisé ({extension}). Formats acceptés : PDF, JPG, PNG")
    if len(contenu) > TAILLE_MAX_OCTETS:
        raise ValueError("Le fichier dépasse la taille maximale autorisée (10 Mo)")

    DOSSIER_UPLOADS.mkdir(parents=True, exist_ok=True)
    nom_fichier = f"{patient_id}_{uuid.uuid4().hex}{extension}"
    chemin = DOSSIER_UPLOADS / nom_fichier
    chemin.write_bytes(contenu)
    return str(chemin)
