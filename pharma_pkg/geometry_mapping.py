"""
PHARMAGEN PRO: Geometry Mapping & Taxonomy Bridge
Deterministic mapping layer between PackagingFamily enums, template IDs (T1/T2/T3),
and render archetypes. Implements the placeholder strategy for roadmap packaging families.
"""

from enum import Enum
from schemas.common import PackagingFamily

class RouteStatus(str, Enum):
    PRODUCTION = "PRODUCTION"
    PLACEHOLDER_ROUTE = "PLACEHOLDER_ROUTE"

# Deterministic mapping table for all 13 PackagingFamily enum values
GEOMETRY_MAPPING = {
    PackagingFamily.BOX_VERTICAL_STANDARD: {
        "template_id": "T1",
        "render_archetype": "carton_box_render",
        "status": RouteStatus.PRODUCTION,
        "is_bottle_override": False
    },
    PackagingFamily.BOX_VERTICAL_SLIM: {
        "template_id": "T2",
        "render_archetype": "slender_carton_render",
        "status": RouteStatus.PRODUCTION,
        "is_bottle_override": False
    },
    PackagingFamily.BOX_HORIZONTAL_FLAT: {
        "template_id": "T3",
        "render_archetype": "long_carton_render",
        "status": RouteStatus.PRODUCTION,
        "is_bottle_override": False
    },
    # The following are future roadmap families mapped via placeholder routing to T1/T2/T3
    PackagingFamily.BOX_SQUARE: {
        "template_id": "T1",
        "render_archetype": "carton_box_render",
        "status": RouteStatus.PLACEHOLDER_ROUTE,
        "is_bottle_override": False
    },
    PackagingFamily.BOTTLE_PLASTIC_ROUND: {
        "template_id": "T1",  # Under Q2, ALL bottles use carton-box templates (T1)
        "render_archetype": "carton_box_render",
        "status": RouteStatus.PLACEHOLDER_ROUTE,
        "is_bottle_override": True
    },
    PackagingFamily.BOTTLE_PLASTIC_TALL: {
        "template_id": "T1",
        "render_archetype": "carton_box_render",
        "status": RouteStatus.PLACEHOLDER_ROUTE,
        "is_bottle_override": True
    },
    PackagingFamily.BOTTLE_GLASS_ROUND: {
        "template_id": "T1",
        "render_archetype": "carton_box_render",
        "status": RouteStatus.PLACEHOLDER_ROUTE,
        "is_bottle_override": True
    },
    PackagingFamily.VIAL_GLASS_SMALL: {
        "template_id": "T1",
        "render_archetype": "carton_box_render",
        "status": RouteStatus.PLACEHOLDER_ROUTE,
        "is_bottle_override": True
    },
    PackagingFamily.TUBE_STANDARD: {
        "template_id": "T3",  # Typically long horizontal packaging
        "render_archetype": "long_carton_render",
        "status": RouteStatus.PLACEHOLDER_ROUTE,
        "is_bottle_override": False
    },
    PackagingFamily.SACHET_FLAT: {
        "template_id": "T1",
        "render_archetype": "carton_box_render",
        "status": RouteStatus.PLACEHOLDER_ROUTE,
        "is_bottle_override": False
    },
    PackagingFamily.BLISTER_CARD: {
        "template_id": "T1",
        "render_archetype": "carton_box_render",
        "status": RouteStatus.PLACEHOLDER_ROUTE,
        "is_bottle_override": False
    },
    PackagingFamily.FOIL_STRIP: {
        "template_id": "T1",
        "render_archetype": "carton_box_render",
        "status": RouteStatus.PLACEHOLDER_ROUTE,
        "is_bottle_override": False
    },
    PackagingFamily.JAR_WIDE: {
        "template_id": "T1",
        "render_archetype": "carton_box_render",
        "status": RouteStatus.PLACEHOLDER_ROUTE,
        "is_bottle_override": False
    },
    PackagingFamily.BOX_MULTIPACK: {
        "template_id": "T_MULTIPACK",
        "render_archetype": "multipack_carton_render",
        "status": RouteStatus.PRODUCTION,
        "is_bottle_override": False
    }
}


def map_geometry_to_family(geom_str: str, product_name: str, package_type: str = "") -> PackagingFamily:
    """
    Deterministic translation from raw packaging geometry strings, product names, and package types
    to the PackagingFamily enum.
    """
    geom_lower = str(geom_str).lower().strip()
    prod_lower = str(product_name).lower().strip()
    pkg_lower = str(package_type).lower().strip()
    
    # 0. Multipack
    if pkg_lower == "multipack" or "multipack" in geom_lower:
        return PackagingFamily.BOX_MULTIPACK
        
    # 1. Boxes
    if "box" in geom_lower or geom_lower == "box" or geom_lower == "":
        if "vertical_slim" in geom_lower or "slim" in geom_lower:
            return PackagingFamily.BOX_VERTICAL_SLIM
        elif "horizontal_flat" in geom_lower or "flat" in geom_lower:
            return PackagingFamily.BOX_HORIZONTAL_FLAT
        elif "square" in geom_lower:
            return PackagingFamily.BOX_SQUARE
        else:
            return PackagingFamily.BOX_VERTICAL_STANDARD
            
    # 2. Bottles
    if "bottle" in geom_lower or "flask" in geom_lower:
        if "tall" in geom_lower:
            return PackagingFamily.BOTTLE_PLASTIC_TALL
        elif "glass" in geom_lower:
            return PackagingFamily.BOTTLE_GLASS_ROUND
        else:
            return PackagingFamily.BOTTLE_PLASTIC_ROUND
            
    # 3. Vials & Ampoules
    if "vial" in geom_lower or "ampoule" in geom_lower:
        return PackagingFamily.VIAL_GLASS_SMALL
        
    # 4. Tubes & Ointments / Creams
    if "tube" in geom_lower or "cream" in prod_lower or "ointment" in prod_lower:
        return PackagingFamily.TUBE_STANDARD
        
    # 5. Sachets
    if "sachet" in geom_lower:
        return PackagingFamily.SACHET_FLAT
        
    # 6. Blisters
    if "blister" in geom_lower:
        return PackagingFamily.BLISTER_CARD
        
    # 7. Foil strips
    if "foil" in geom_lower or "strip" in geom_lower:
        return PackagingFamily.FOIL_STRIP
        
    # 8. Jars
    if "jar" in geom_lower:
        return PackagingFamily.JAR_WIDE
        
    # Default fallback
    return PackagingFamily.BOX_VERTICAL_STANDARD
