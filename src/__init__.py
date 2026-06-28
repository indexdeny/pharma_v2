"""PharmaGen PRO — unified pipeline package.

Modules:
    utils                : config loading, path resolution, logging helpers
    passport_generator   : Stage 1 — JSON passports -> Markdown prompts (ex pass_tomd.py)
    rpa_orchestrator     : Stage 2 — Markdown -> raw PNG via Selenium/Gemini (ex gemini_image_generator.py)
    image_processor      : Stage 3 — raw PNG -> final WEBP (ex webp_converter.py)

The original root-level scripts (pass_tomd.py, gemini_image_generator.py,
webp_converter.py) are kept as thin compatibility shims that re-export from here.
All orchestration goes through ../main.py.
"""

__version__ = "1.0.0"
