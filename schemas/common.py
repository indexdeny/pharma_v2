from pydantic import BaseModel, Field, model_validator
from typing import Literal, List, Optional
from enum import Enum

class UVBox(BaseModel):
    """Нормализованные координаты UV [0, 1]. Для CV-слоя."""
    y1: float = Field(..., ge=0.0, le=1.0)
    x1: float = Field(..., ge=0.0, le=1.0)
    y2: float = Field(..., ge=0.0, le=1.0)
    x2: float = Field(..., ge=0.0, le=1.0)

    @model_validator(mode='after')
    def validate_geometry(self) -> 'UVBox':
        if self.y1 >= self.y2:
            raise ValueError(f"y1 must be less than y2")
        if self.x1 >= self.x2:
            raise ValueError(f"x1 must be less than x2")
        return self

AllowedFonts = Literal[
    "helvetica_bold",
    "helvetica_regular",
    "din_condensed",
    "frutiger",
    "gotham",
    "roboto"
]

class PackagingFamily(str, Enum):
    BOX_VERTICAL_STANDARD = "box_vertical_standard"
    BOX_VERTICAL_SLIM = "box_vertical_slim"
    BOX_HORIZONTAL_FLAT = "box_horizontal_flat"
    BOX_SQUARE = "box_square"
    BOTTLE_PLASTIC_ROUND = "bottle_plastic_round"
    BOTTLE_PLASTIC_TALL = "bottle_plastic_tall"
    BOTTLE_GLASS_ROUND = "bottle_glass_round"
    VIAL_GLASS_SMALL = "vial_glass_small"
    TUBE_STANDARD = "tube_standard"
    SACHET_FLAT = "sachet_flat"
    BLISTER_CARD = "blister_card"
    FOIL_STRIP = "foil_strip"
    JAR_WIDE = "jar_wide"
    BOX_MULTIPACK = "box_multipack"

# [STATUS: ROADMAP_ONLY] — Unused in production; target for future multi-archetype scene rendering
SceneArchetype = Literal[
    "slim_blister_carton",
    "thick_blister_carton",
    "hdpe_bottle_carton",
    "retail_bottle",
    "wallet_blister",
    "hospital_pack",
    "sachet_carton",
    "tube_carton",
    "vial_tray_carton"
]

# [STATUS: ROADMAP_ONLY] — Unused in production; target for future typographic render verification
class TypographySpec(BaseModel):
    font_family: AllowedFonts
    font_weight: int = Field(default=400, ge=100, le=900)
    case: Literal["uppercase", "lowercase", "titlecase", "original"] = "original"
    tracking: float = Field(default=0.0)
    max_font_scale: float = Field(default=1.0, ge=0.1, le=2.0)
    min_font_scale: float = Field(default=0.3, ge=0.05, le=1.0)
    line_clamp: int = Field(default=1, ge=1, le=10)
    allow_multiline: bool = False

class ObservedPalette(BaseModel):
    dominant_colors: List[str]
    detected_background: Optional[str] = None
    color_confidence: float = Field(default=1.0, ge=0.0, le=1.0)

# [STATUS: ROADMAP_ONLY] — Unused in production; target for future palette validation matching
class RenderPalette(BaseModel):
    primary_bg: str = Field(default="#FFFFFF", pattern=r'^#(?:[0-9a-fA-F]{3}){1,2}$')
    text_primary: str = Field(default="#000000", pattern=r'^#(?:[0-9a-fA-F]{3}){1,2}$')
    accent_color: Optional[str] = Field(None, pattern=r'^#(?:[0-9a-fA-F]{3}){1,2}$')

# [STATUS: ROADMAP_ONLY] — Unused in production; target for future detailed material rendering specifications
class SurfaceFinishSpec(BaseModel):
    lamination: Literal["matte", "glossy"]
    spot_uv: bool = False
    foil: bool = False
    embossing: bool = False

# [STATUS: ROADMAP_ONLY] — Unused in production; target for future normalized coordinate bounding box mapping
class NormalizedBox(BaseModel):
    x: float
    y: float
    width: float
    height: float
    anchor: Literal["top_left", "center"] = "center"
