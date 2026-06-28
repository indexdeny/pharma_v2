"""Compatibility shim — the implementation now lives in src/rpa_orchestrator.py.

Kept so the legacy command `python gemini_image_generator.py [--all|--limit|--from|--estimate]`
still works. Prefer the unified entry point:  python main.py --render-only
"""
from src.rpa_orchestrator import *         # noqa: F401,F403  (re-export public API)
from src.rpa_orchestrator import main

if __name__ == "__main__":
    main()
