from fastapi import APIRouter, Depends

from app.bll.interfaces.i_import_service import IImportService
from app.core.config import settings
from app.core.dependencies import get_import_service

router = APIRouter(prefix="/import", tags=["import"])


@router.post("/")
def import_data(service: IImportService = Depends(get_import_service)):
    result = service.import_from_csv(settings.CSV_FILE_PATH)
    return {"status": "success", "imported": result}


@router.get("/health")
def health_check():
    return {"status": "ok"}
