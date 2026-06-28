"""Compatibility shim — the implementation now lives in src/image_processor.py.

Kept so the legacy command `python webp_converter.py` still works.
Prefer the unified entry point:  python main.py --process-images-only
"""
from src.image_processor import *          # noqa: F401,F403  (re-export public API)
from src.image_processor import main

if __name__ == "__main__":
    main()
