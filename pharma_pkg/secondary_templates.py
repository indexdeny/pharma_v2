from dataclasses import dataclass

@dataclass
class SecondaryPackageTemplate:
    name: str               # "TEMPLATE_BLISTER_BOX" etc.
    box_width_mm: float
    box_height_mm: float
    box_depth_mm: float
    render_shape: str       # всегда "medicine_box" — тип коробки не меняется
