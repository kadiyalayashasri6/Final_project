from pydantic import BaseModel, Field
from typing import Optional


class ScanResponse(BaseModel):
    status: str = Field(..., example="safe")
    upi_id: Optional[str] = Field(None, example="merchant@ybl")
    merchant: Optional[str] = Field(None, example="ABC Store")
    provider: Optional[str] = Field(None, example="PhonePe")
    risk_score: Optional[int] = Field(None, example=20)
    message: Optional[str] = Field(None, example="Valid UPI QR")


class ErrorResponse(BaseModel):
    status: str = "error"
    message: str