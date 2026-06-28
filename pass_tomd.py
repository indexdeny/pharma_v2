"""Compatibility shim — the implementation now lives in src/passport_generator.py.

Kept so that:
  * the legacy command `python pass_tomd.py` still works, and
  * `from pass_tomd import agent_1_router, TEMPLATE_MAP, ...` (used by
    generate_architecture_snapshot.py) keeps resolving.

Prefer the unified entry point:  python main.py --passports-only
"""
from src.passport_generator import *        # noqa: F401,F403  (re-export public API)
from src.passport_generator import main

if __name__ == "__main__":
    main()
