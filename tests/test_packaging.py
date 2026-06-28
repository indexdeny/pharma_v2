import unittest
from pharma_pkg.primary_classifier import PrimaryPackage, PrimaryPackageType
from pharma_pkg.secondary_templates import SecondaryPackageTemplate
from pharma_pkg.dimension_resolver import resolve_secondary, validate_fit

class TestPackaging(unittest.TestCase):
    def test_positive_bottle(self):
        # bottle (35×35×95mm) -> TEMPLATE_BOTTLE_BOX, box 45×45×110mm, render_shape = "medicine_box"
        primary = PrimaryPackage(
            type=PrimaryPackageType.BOTTLE,
            geometry="cylindrical",
            width_mm=35,
            height_mm=95,
            depth_mm=35
        )
        sec = resolve_secondary(primary)
        self.assertEqual(sec.name, "TEMPLATE_BOTTLE_BOX")
        self.assertEqual(sec.box_width_mm, 45) # 35 + 10 = 45
        self.assertEqual(sec.box_height_mm, 110) # 95 + 10 * 1.5 = 110
        self.assertEqual(sec.box_depth_mm, 45)
        self.assertEqual(sec.render_shape, "medicine_box")
        
        # Verify validate_fit passes
        validate_fit(primary, sec)

    def test_positive_nasal_spray(self):
        # nasal_spray (25×25×120mm) -> TEMPLATE_BOTTLE_BOX (classified as BOTTLE)
        primary = PrimaryPackage(
            type=PrimaryPackageType.BOTTLE,
            geometry="cylindrical",
            width_mm=25,
            height_mm=120,
            depth_mm=25
        )
        sec = resolve_secondary(primary)
        self.assertEqual(sec.name, "TEMPLATE_BOTTLE_BOX")
        self.assertEqual(sec.box_width_mm, 35) # 25 + 10 = 35
        self.assertEqual(sec.box_height_mm, 135) # 120 + 15 = 135
        self.assertEqual(sec.box_depth_mm, 35)
        validate_fit(primary, sec)

    def test_positive_syringe(self):
        # syringe (15×15×150mm) -> TEMPLATE_SYRINGE_BOX, elongated box
        primary = PrimaryPackage(
            type=PrimaryPackageType.SYRINGE,
            geometry="elongated",
            width_mm=150,
            height_mm=15,
            depth_mm=15
        )
        sec = resolve_secondary(primary)
        self.assertEqual(sec.name, "TEMPLATE_SYRINGE_BOX")
        self.assertEqual(sec.box_width_mm, 23) # depth 15 + clearance 8 = 23
        self.assertEqual(sec.box_height_mm, 23) # height 15 + clearance 8 = 23
        self.assertEqual(sec.box_depth_mm, 158) # width 150 + clearance 8 = 158
        validate_fit(primary, sec)

    def test_positive_blister(self):
        # blister (85×55×8mm) -> TEMPLATE_BLISTER_BOX, compact flat box
        primary = PrimaryPackage(
            type=PrimaryPackageType.BLISTER,
            geometry="flat_rectangular",
            width_mm=85,
            height_mm=55,
            depth_mm=8
        )
        sec = resolve_secondary(primary)
        self.assertEqual(sec.name, "TEMPLATE_BLISTER_BOX")
        self.assertEqual(sec.box_width_mm, 90) # 85 + 5 = 90
        self.assertEqual(sec.box_height_mm, 57.0) # 55 + 5 // 2 = 57
        self.assertEqual(sec.box_depth_mm, 13) # 8 + 5 = 13
        validate_fit(primary, sec)

    def test_negative_height_overflow(self):
        # primary_height > box_height -> PackageFitError (ValueError)
        primary = PrimaryPackage(
            type=PrimaryPackageType.BLISTER,
            geometry="flat_rectangular",
            width_mm=85,
            height_mm=55,
            depth_mm=8
        )
        # Manually create a secondary template that is too short
        sec = SecondaryPackageTemplate(
            name="TEMPLATE_BLISTER_BOX",
            box_width_mm=90,
            box_height_mm=50, # 50 < 55 (primary height)
            box_depth_mm=13,
            render_shape="medicine_box"
        )
        with self.assertRaises(ValueError) as context:
            validate_fit(primary, sec)
        self.assertIn("primary_height", str(context.exception))

    def test_negative_volume_overflow(self):
        # primary_volume > secondary_volume -> PackageFitError
        primary = PrimaryPackage(
            type=PrimaryPackageType.BLISTER,
            geometry="flat_rectangular",
            width_mm=85,
            height_mm=55,
            depth_mm=8
        )
        # Create secondary template with smaller volume overall
        sec = SecondaryPackageTemplate(
            name="TEMPLATE_BLISTER_BOX",
            box_width_mm=90,
            box_height_mm=57,
            box_depth_mm=5, # volume: 90 * 57 * 5 = 25650. primary volume: 85 * 55 * 8 = 37400.
            render_shape="medicine_box"
        )
        with self.assertRaises(ValueError) as context:
            validate_fit(primary, sec)
        self.assertIn("primary_volume", str(context.exception))

    def test_negative_invalid_dimensions(self):
        # width_mm = -10 -> ValueError from __post_init__
        with self.assertRaises(ValueError):
            PrimaryPackage(
                type=PrimaryPackageType.BLISTER,
                geometry="flat_rectangular",
                width_mm=-10,
                height_mm=55,
                depth_mm=8
            )

if __name__ == "__main__":
    unittest.main()
