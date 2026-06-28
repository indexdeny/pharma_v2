"""PharmaGen PRO — shared utilities.

Central place for:
  * PROJECT_ROOT anchoring (so relative paths work regardless of CWD)
  * config.yaml loading with environment overrides
  * logging setup (rich console + file), with graceful fallback if rich is absent

The hard-coded defaults below mirror the original scripts' constants EXACTLY,
so behaviour is byte-for-byte identical when config.yaml is missing.
"""
from __future__ import annotations

import os
import sys
import copy
import logging
from pathlib import Path
from functools import lru_cache

# ── Project root = the parent directory of this src/ package ─────────────────
PROJECT_ROOT = Path(__file__).resolve().parents[1]

DEFAULT_CONFIG_FILENAME = "config.yaml"

# These defaults reproduce the legacy hard-coded constants verbatim.
_DEFAULTS = {
    "paths": {
        "ssot_sku_csv":        "SSOT/SKU.csv",
        "ssot_master_json":    "SSOT/master.json",
        "ssot_design_specs":   "SSOT/master_pharma_design_specs.json",
        "passports_json":      "pipeline/passports",
        "passports_md":        "pipeline/passports.markdown",
        "renders_raw":         "render_output/raw",
        "renders_failed":      "render_output/failed",
        "renders_failed_logs": "render_output/failed_logs",
        "renders_final":       "output",
        "logs":                "logs",
        "failures_log":        "verification_failures.log",
        "progress_file":       "gemini_rpa_progress_v23.txt",
    },
    "rpa": {
        "browser_profile_dir":      r"LOCAL_HOME\.gemini\antigravity-browser-profile\Profile 1",
        "browser_profile_name":     "Profile 1",
        "downloads_dir":            r"LOCAL_HOME\Downloads",
        "gemini_url":               "https://gemini.google.com/app",
        "headless":                 False,
        "batch_size":               1,
        "image_generation_timeout": 180,
        "download_timeout":         60,
        "ready_timeout":            30,
        "post_click_delay":         2,
    },
    "image_processor": {
        "source_dir":       "render_output/raw",
        "output_dir":       "output",
        "target_size":      [1600, 1600],
        "max_file_size_kb": 500,
    },
    "pipeline": {
        # stage-level retry attempts for the (transient-prone) render stage
        "render_retries": 1,
    },
    "logging": {
        "level": "INFO",
    },
}


def resolve_path(p) -> Path:
    """Resolve a possibly-relative path against PROJECT_ROOT (absolute paths are kept)."""
    pp = Path(p)
    return pp if pp.is_absolute() else (PROJECT_ROOT / pp)


def _deep_merge(base: dict, override: dict) -> dict:
    out = copy.deepcopy(base)
    for k, v in (override or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


@lru_cache(maxsize=None)
def _load_file_config(config_path: str | None, env_config: str | None) -> dict:
    """Pure (defaults + config.yaml) merge — cached. Contains NO runtime env
    overrides, and the env-derived config path is part of the cache key so a
    changed PHARMAGEN_CONFIG never returns a stale file.
    """
    path = config_path or env_config
    cfg_file = resolve_path(path) if path else (PROJECT_ROOT / DEFAULT_CONFIG_FILENAME)

    file_cfg: dict = {}
    if cfg_file.exists():
        try:
            import yaml  # PyYAML
            with open(cfg_file, "r", encoding="utf-8") as f:
                file_cfg = yaml.safe_load(f) or {}
        except ImportError:
            print("[WARN] PyYAML not installed; using built-in defaults (pip install pyyaml).")
            file_cfg = {}
        except Exception as e:  # malformed yaml -> defaults, never crash a stage
            print(f"[WARN] Could not parse {cfg_file}: {e}. Using built-in defaults.")
            file_cfg = {}

    return _deep_merge(_DEFAULTS, file_cfg)


def load_config(config_path: str | None = None) -> dict:
    """Load config.yaml merged over defaults, then apply environment overrides.

    File resolution order:
      1. explicit ``config_path``
      2. ``PHARMAGEN_CONFIG`` environment variable
      3. ``<PROJECT_ROOT>/config.yaml``
    A missing/unparseable file falls back to defaults (identical to legacy
    behaviour). Env overrides (PHARMAGEN_HEADLESS / PHARMAGEN_DEBUG) are applied
    per-call to a fresh deep copy, so they are never cached or mutated in place.
    """
    cfg = copy.deepcopy(_load_file_config(config_path, os.environ.get("PHARMAGEN_CONFIG")))

    # ── Environment overrides (main.py sets these for subprocess stages) ─────
    headless_env = os.environ.get("PHARMAGEN_HEADLESS")
    if headless_env is not None and headless_env != "":
        cfg["rpa"]["headless"] = headless_env.lower() in ("1", "true", "yes", "on")
    debug_env = os.environ.get("PHARMAGEN_DEBUG")
    if debug_env and debug_env.lower() in ("1", "true", "yes", "on"):
        cfg["logging"]["level"] = "DEBUG"

    return cfg


def get_path(cfg: dict, key: str) -> Path:
    """Absolute Path for ``paths.<key>``, anchored to PROJECT_ROOT."""
    return resolve_path(cfg["paths"][key])


# ── Logging ──────────────────────────────────────────────────────────────────

def setup_logging(level: str = "INFO", log_dir=None, run_name: str = "pharmagen",
                  to_file: bool = True):
    """Configure the root logger with a rich console handler (fallback: plain) and
    an optional file handler under ``log_dir``. Returns (logger, log_path|None)."""
    lvl = getattr(logging, str(level).upper(), logging.INFO)
    root = logging.getLogger()
    root.setLevel(lvl)
    for h in list(root.handlers):          # avoid duplicate handlers on re-call
        root.removeHandler(h)

    # console handler
    try:
        from rich.logging import RichHandler
        console = RichHandler(rich_tracebacks=True, show_path=False, markup=False,
                              log_time_format="%H:%M:%S")
    except ImportError:
        console = logging.StreamHandler(sys.stdout)
        console.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s",
                                               "%H:%M:%S"))
    console.setLevel(lvl)
    root.addHandler(console)

    log_path = None
    if to_file:
        ld = resolve_path(log_dir) if log_dir else (PROJECT_ROOT / "logs")
        ld.mkdir(parents=True, exist_ok=True)
        log_path = ld / f"{run_name}.log"
        fh = logging.FileHandler(log_path, encoding="utf-8")
        fh.setLevel(lvl)
        fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
        root.addHandler(fh)

    return logging.getLogger("pharmagen"), log_path
