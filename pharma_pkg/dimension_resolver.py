import yaml
from pathlib import Path
from pharma_pkg.primary_classifier import PrimaryPackage, PrimaryPackageType
from pharma_pkg.secondary_templates import SecondaryPackageTemplate

def load_mapping() -> dict:
    path = Path(__file__).parent / "package_mapping.yaml"
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def resolve_secondary(primary: PrimaryPackage) -> SecondaryPackageTemplate:
    mapping = load_mapping()
    cfg = mapping.get(primary.type.value)
    if not cfg:
        raise KeyError(f"No mapping found for primary package type: {primary.type}")
        
    c = cfg["clearance_mm"]

    if primary.type == PrimaryPackageType.BLISTER:
        return SecondaryPackageTemplate(
            name=cfg["template"],
            box_width_mm=primary.width_mm + c,
            box_height_mm=primary.height_mm + c // 2,
            box_depth_mm=primary.depth_mm + c,
            render_shape="medicine_box"
        )
    elif primary.type == PrimaryPackageType.SYRINGE:
        return SecondaryPackageTemplate(
            name=cfg["template"],
            box_width_mm=primary.depth_mm + c,
            box_height_mm=primary.height_mm + c,
            box_depth_mm=primary.width_mm + c,
            render_shape="medicine_box"
        )
    elif primary.type == PrimaryPackageType.BOTTLE:
        diameter = max(primary.width_mm, primary.depth_mm)
        return SecondaryPackageTemplate(
            name=cfg["template"],
            box_width_mm=diameter + c,
            box_height_mm=primary.height_mm + c * 1.5,
            box_depth_mm=diameter + c,
            render_shape="medicine_box"
        )
    else:
        raise ValueError(f"Unknown primary package type: {primary.type}")

def validate_fit(primary: PrimaryPackage, secondary: SecondaryPackageTemplate) -> None:
    errors = []
    pv = primary.width_mm * primary.height_mm * primary.depth_mm
    sv = secondary.box_width_mm * secondary.box_height_mm * secondary.box_depth_mm

    if pv > sv:
        errors.append(f"primary_volume {pv:.0f}mm³ > secondary_volume {sv:.0f}mm³")
        
    # Validation check respecting the alignment mappings in resolve_secondary
    if primary.type == PrimaryPackageType.SYRINGE:
        if primary.depth_mm > secondary.box_width_mm:
            errors.append(f"primary_depth {primary.depth_mm}mm > box_width {secondary.box_width_mm}mm")
        if primary.height_mm > secondary.box_height_mm:
            errors.append(f"primary_height {primary.height_mm}mm > box_height {secondary.box_height_mm}mm")
        if primary.width_mm > secondary.box_depth_mm:
            errors.append(f"primary_width {primary.width_mm}mm > box_depth {secondary.box_depth_mm}mm")
    else:
        if primary.width_mm > secondary.box_width_mm:
            errors.append(f"primary_width {primary.width_mm}mm > box_width {secondary.box_width_mm}mm")
        if primary.height_mm > secondary.box_height_mm:
            errors.append(f"primary_height {primary.height_mm}mm > box_height {secondary.box_height_mm}mm")
        if primary.depth_mm > secondary.box_depth_mm:
            errors.append(f"primary_depth {primary.depth_mm}mm > box_depth {secondary.box_depth_mm}mm")

    if errors:
        raise ValueError(f"PackageFitError: {'; '.join(errors)}. Recalculate dimensions.")

def estimate_primary_from_secondary(package_type: PrimaryPackageType, sec_w: float, sec_h: float, sec_d: float) -> PrimaryPackage:
    """Estimates primary package dimensions by reversing the secondary packaging dimensions logic."""
    mapping = load_mapping()
    cfg = mapping[package_type.value]
    c = cfg["clearance_mm"]

    if package_type == PrimaryPackageType.BLISTER:
        w = max(5.0, sec_w - c)
        h = max(5.0, sec_h - c / 2.0)
        d = max(1.0, sec_d - c)
        return PrimaryPackage(
            type=package_type,
            geometry="flat_rectangular",
            width_mm=w,
            height_mm=h,
            depth_mm=d
        )
    elif package_type == PrimaryPackageType.SYRINGE:
        # Reverse mapping:
        # box_width_mm = primary.depth_mm + c  => primary.depth_mm = box_width_mm - c
        # box_height_mm = primary.height_mm + c => primary.height_mm = box_height_mm - c
        # box_depth_mm = primary.width_mm + c   => primary.width_mm = box_depth_mm - c
        d = max(5.0, sec_w - c)
        h = max(5.0, sec_h - c)
        w = max(5.0, sec_d - c)
        return PrimaryPackage(
            type=package_type,
            geometry="elongated",
            width_mm=w,
            height_mm=h,
            depth_mm=d
        )
    elif package_type == PrimaryPackageType.BOTTLE:
        # Reverse mapping:
        # box_width_mm = diameter + c   => diameter = box_width_mm - c
        # box_height_mm = primary.height_mm + c * 1.5 => primary.height_mm = box_height_mm - c * 1.5
        diameter_w = max(5.0, sec_w - c)
        diameter_d = max(5.0, sec_d - c)
        diameter = max(diameter_w, diameter_d)
        h = max(5.0, sec_h - c * 1.5)
        return PrimaryPackage(
            type=package_type,
            geometry="cylindrical",
            width_mm=diameter,
            height_mm=h,
            depth_mm=diameter
        )
    else:
        raise ValueError(f"Unknown package type: {package_type}")
