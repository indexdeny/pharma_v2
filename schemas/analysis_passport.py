from pydantic import BaseModel, Field
from typing import Dict, Optional
from schemas.common import UVBox, ObservedPalette, PackagingFamily

class ObservedZone(BaseModel):
    raw_text: Optional[str] = None
    bbox: UVBox
    ocr_confidence: float = Field(ge=0.0, le=1.0)
    visual_score: float = Field(ge=0.0, le=1.0)

class AnalysisPassport(BaseModel):
    image_path: str
    detected_family: PackagingFamily
    zones: Dict[str, ObservedZone]
    palette: ObservedPalette
