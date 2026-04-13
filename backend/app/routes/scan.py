from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.qr_service import scan_qr
from app.services.upi_validator import validate_upi

router = APIRouter()


@router.post("/scan")
async def scan_qr_code(file: UploadFile = File(...)):
    """
    Scan QR image and validate payment safety
    """
    try:
        content = await file.read()

        qr_data = scan_qr(content)

        result = validate_upi(qr_data)

        return result

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")