from enum import Enum
from dataclasses import dataclass

class PrimaryPackageType(str, Enum):
    BLISTER  = "BLISTER"   # таблетки, капсулы, плоские формы
    SYRINGE  = "SYRINGE"   # шприцы, автоинъекторы, продолговатые формы
    BOTTLE   = "BOTTLE"    # флаконы, бутылки, назальные спреи, дропперы

@dataclass
class PrimaryPackage:
    type: PrimaryPackageType
    geometry: str           # "cylindrical" | "flat_rectangular" | "elongated"
    width_mm: float
    height_mm: float
    depth_mm: float

    def __post_init__(self):
        # Convert dimensions to float in case they were parsed as strings
        self.width_mm = float(self.width_mm)
        self.height_mm = float(self.height_mm)
        self.depth_mm = float(self.depth_mm)
        
        if self.width_mm <= 0 or self.height_mm <= 0 or self.depth_mm <= 0:
            raise ValueError("Dimensions must be positive values.")
