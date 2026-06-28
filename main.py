#!/usr/bin/env python3
"""PharmaGen PRO — unified pipeline entry point.

One command runs the whole render factory end to end:

    passports (JSON -> MD)  ->  render (MD -> raw PNG via Gemini RPA)  ->  final WEBP

Examples:
    python main.py --full                       # whole catalogue, all 3 stages
    python main.py --full --resume              # continue after an interruption
    python main.py --passports-only             # only Stage 1
    python main.py --render-only --limit 5      # render first 5 unprocessed
    python main.py --render-only --from 50-min  # render starting at stem 50-min
    python main.py --process-images-only --resume
    python main.py --full --debug               # verbose logging

Each stage runs as an isolated subprocess so its behaviour is byte-for-byte the
same as running the original script — main.py only adds orchestration, logging,
resume, retries and a final report. Stages are sequential because each consumes
the previous stage's output.
"""
from __future__ import annotations

import os
import sys
import time
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

# Make the project root importable regardless of where main.py is invoked from.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.utils import (  # noqa: E402
    PROJECT_ROOT, load_config, get_path, resolve_path, setup_logging,
)

# ── Stage registry ────────────────────────────────────────────────────────────
STAGE_PASSPORTS = "passports"
STAGE_RENDER    = "render"
STAGE_PROCESS   = "process-images"

MODULE = {
    STAGE_PASSPORTS: "src.passport_generator",
    STAGE_RENDER:    "src.rpa_orchestrator",
    STAGE_PROCESS:   "src.image_processor",
}


# ── CLI ───────────────────────────────────────────────────────────────────────
def parse_args(argv=None):
    p = argparse.ArgumentParser(
        prog="main.py",
        description="PharmaGen PRO — unified pipeline (passports -> render -> final images).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    mode = p.add_mutually_exclusive_group()
    mode.add_argument("--full", action="store_true",
                      help="Run all stages: passports -> render -> process-images (default)")
    mode.add_argument("--passports-only", action="store_true",
                      help="Only Stage 1: JSON passports -> Markdown prompts")
    mode.add_argument("--render-only", action="store_true",
                      help="Only Stage 2: Markdown -> raw PNG via Gemini RPA")
    mode.add_argument("--process-images-only", action="store_true",
                      help="Only Stage 3: raw PNG -> final WEBP")

    p.add_argument("--resume", action="store_true",
                   help="Skip already-completed work (no duplicated output)")
    p.add_argument("--headless", action="store_true",
                   help="Force headless Chrome for render (WARNING: Gemini usually blocks "
                        "headless image generation — debug only)")
    p.add_argument("--debug", action="store_true", help="Verbose DEBUG logging")
    p.add_argument("--limit", type=int, default=None,
                   help="Render stage: cap number of passports (default for full/render: ALL)")
    p.add_argument("--from", dest="from_stem", default=None,
                   help="Render stage: start from a passport stem, e.g. 50-min")
    p.add_argument("--config", default=None,
                   help="Path to a config.yaml (overrides the default project config)")
    return p.parse_args(argv)


def resolve_stages(args):
    if args.passports_only:
        return [STAGE_PASSPORTS]
    if args.render_only:
        return [STAGE_RENDER]
    if args.process_images_only:
        return [STAGE_PROCESS]
    return [STAGE_PASSPORTS, STAGE_RENDER, STAGE_PROCESS]  # --full (default)


def build_cmd(stage, args):
    cmd = [sys.executable, "-m", MODULE[stage]]
    if stage == STAGE_RENDER:
        if args.limit is not None:
            cmd += ["--limit", str(args.limit)]
        else:
            cmd += ["--all"]          # full/render default = entire remaining catalogue
        if args.from_stem:
            cmd += ["--from", args.from_stem]
    elif stage == STAGE_PROCESS:
        if args.resume:
            cmd += ["--resume"]
    # passports stage takes no flags (resume handled here in the orchestrator)
    return cmd


# ── Pre-flight validation ─────────────────────────────────────────────────────
def _count(path: Path, pattern: str) -> int:
    return len(list(path.glob(pattern))) if path.exists() else 0


def preflight(stages, cfg, log) -> bool:
    import json
    ok = True

    if STAGE_PASSPORTS in stages:
        # SSOT integrity (only the passport stage depends on the SSOT)
        for key, kind in (("ssot_sku_csv", "csv"),
                          ("ssot_master_json", "json"),
                          ("ssot_design_specs", "json")):
            path = get_path(cfg, key)
            if not path.exists():
                log.error(f"SSOT missing: {path}"); ok = False; continue
            if path.stat().st_size == 0:
                log.error(f"SSOT empty: {path}"); ok = False; continue
            if kind == "json":
                try:
                    with open(path, encoding="utf-8") as f:
                        json.load(f)
                except Exception as e:
                    log.error(f"SSOT corrupt JSON {path.name}: {e}"); ok = False
        jdir = get_path(cfg, "passports_json")
        n = _count(jdir, "*.json")
        if n == 0:
            log.error(f"No JSON passports in {jdir} — nothing to convert."); ok = False
        else:
            log.info(f"Pre-flight: {n} JSON passports found.")

    if STAGE_RENDER in stages:
        mdir = get_path(cfg, "passports_md")
        n = _count(mdir, "*.md")
        if n == 0 and STAGE_PASSPORTS not in stages:
            log.error(f"No Markdown passports in {mdir} — run the passports stage first."); ok = False
        prof = Path(cfg["rpa"]["browser_profile_dir"])
        if not prof.exists():
            log.warning(f"Browser profile not found: {prof}\n"
                        f"           The render stage needs a logged-in Gemini session in that profile.")

    if STAGE_PROCESS in stages:
        rdir = get_path(cfg, "renders_raw")
        n = _count(rdir, "*.png")
        if n == 0 and STAGE_RENDER not in stages:
            log.error(f"No raw PNG renders in {rdir} — run the render stage first."); ok = False

    return ok


def should_skip_passports(cfg, log) -> bool:
    """Resume: skip Stage 1 if every JSON passport already has a Markdown file."""
    n_json = _count(get_path(cfg, "passports_json"), "*.json")
    n_md = _count(get_path(cfg, "passports_md"), "*.md")
    if n_json > 0 and n_md >= n_json:
        log.info(f"[resume] Passports already generated ({n_md} MD >= {n_json} JSON) — skipping Stage 1.")
        return True
    return False


# ── Stage execution ───────────────────────────────────────────────────────────
def _stream(cmd, env, stage, log) -> int:
    try:
        proc = subprocess.Popen(
            cmd, cwd=str(PROJECT_ROOT), env=env,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, encoding="utf-8", errors="replace", bufsize=1,
        )
    except Exception as e:
        log.error(f"[{stage}] failed to launch subprocess: {e}")
        return 1
    try:
        assert proc.stdout is not None
        for line in proc.stdout:
            line = line.rstrip("\n")
            if line:
                log.info(f"[{stage}] {line}")
        proc.wait()
    except KeyboardInterrupt:
        log.warning(f"[{stage}] interrupted — terminating subprocess...")
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except Exception:
            proc.kill()
        raise
    return proc.returncode


def run_stage(stage, args, cfg, env, log) -> dict:
    cmd = build_cmd(stage, args)
    attempts = 1
    if stage == STAGE_RENDER:
        attempts = max(1, int(cfg["pipeline"].get("render_retries", 1)) + 1)
    last_rc = None
    start = time.time()
    for attempt in range(1, attempts + 1):
        if attempt > 1:
            log.warning(f"[{stage}] retry {attempt - 1}/{attempts - 1} after failure (rc={last_rc})...")
        log.info(f"[{stage}] $ {' '.join(cmd)}")
        last_rc = _stream(cmd, env, stage, log)
        if last_rc == 0:
            break
    return {"stage": stage, "rc": last_rc, "ok": last_rc == 0,
            "duration": time.time() - start}


# ── Reporting ─────────────────────────────────────────────────────────────────
def artifact_counts(cfg) -> dict:
    return {
        "JSON passports": _count(get_path(cfg, "passports_json"), "*.json"),
        "MD passports":   _count(get_path(cfg, "passports_md"), "*.md"),
        "Raw PNG":        _count(get_path(cfg, "renders_raw"), "*.png"),
        "Final WEBP":     _count(get_path(cfg, "renders_final"), "*.webp"),
    }


_STATUS_LABEL = {"ok": "✅ OK", "failed": "❌ FAILED", "skipped": "⏭️  SKIPPED"}


def print_summary(results, counts, log_path, total_dur, log):
    try:
        from rich.console import Console
        from rich.table import Table
        console = Console()

        t = Table(title="PharmaGen PRO — Run Summary", show_lines=False)
        t.add_column("Stage"); t.add_column("Status"); t.add_column("Duration", justify="right"); t.add_column("RC", justify="right")
        for r in results:
            dur = f"{r['duration']:.1f}s" if r.get("duration") else "-"
            t.add_row(r["stage"], _STATUS_LABEL.get(r["status"], r["status"]), dur,
                      str(r.get("rc") if r.get("rc") is not None else "-"))
        console.print(t)

        ct = Table(title="Artifacts on disk", show_lines=False)
        ct.add_column("Type"); ct.add_column("Count", justify="right")
        for k, v in counts.items():
            ct.add_row(k, str(v))
        console.print(ct)
    except ImportError:
        log.info("─" * 50)
        log.info("RUN SUMMARY")
        for r in results:
            dur = f"{r['duration']:.1f}s" if r.get("duration") else "-"
            log.info(f"  {r['stage']:<16} {_STATUS_LABEL.get(r['status'], r['status']):<12} {dur:>8}  rc={r.get('rc')}")
        log.info("ARTIFACTS")
        for k, v in counts.items():
            log.info(f"  {k:<16} {v}")
        log.info("─" * 50)

    log.info(f"Total wall time: {total_dur:.1f}s")
    if log_path:
        log.info(f"Full log: {log_path}")


# ── Main ──────────────────────────────────────────────────────────────────────
def main(argv=None) -> int:
    args = parse_args(argv)

    # Propagate flags to subprocess stages via environment (read by src/utils).
    if args.config:
        os.environ["PHARMAGEN_CONFIG"] = str(resolve_path(args.config))
    if args.headless:
        os.environ["PHARMAGEN_HEADLESS"] = "1"
    if args.debug:
        os.environ["PHARMAGEN_DEBUG"] = "1"

    cfg = load_config(os.environ.get("PHARMAGEN_CONFIG"))
    level = "DEBUG" if args.debug else cfg["logging"]["level"]
    run_name = f"pharmagen_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    log, log_path = setup_logging(level=level, log_dir=get_path(cfg, "logs"), run_name=run_name)

    stages = resolve_stages(args)
    mode_label = "full" if len(stages) == 3 else ", ".join(stages)
    log.info("=" * 70)
    log.info("  PharmaGen PRO — unified pipeline")
    log.info(f"  Mode:    {mode_label}")
    log.info(f"  Flags:   resume={args.resume}  headless={args.headless}  debug={args.debug}"
             + (f"  limit={args.limit}" if args.limit is not None else "")
             + (f"  from={args.from_stem}" if args.from_stem else ""))
    log.info(f"  Root:    {PROJECT_ROOT}")
    log.info(f"  Config:  {os.environ.get('PHARMAGEN_CONFIG', '(config.yaml + built-in defaults)')}")
    log.info("=" * 70)
    if args.headless:
        log.warning("--headless requested: Gemini typically BLOCKS image generation in headless "
                    "mode. Use only for debugging the render stage.")

    if not preflight(stages, cfg, log):
        log.error("Pre-flight checks failed. Aborting before any stage runs.")
        return 2

    child_env = os.environ.copy()
    child_env.setdefault("PYTHONIOENCODING", "utf-8")
    child_env["PYTHONUNBUFFERED"] = "1"

    results = []
    overall_start = time.time()
    aborted = False

    try:
        for stage in stages:
            if aborted:
                results.append({"stage": stage, "status": "skipped", "duration": 0, "rc": None})
                continue
            if stage == STAGE_PASSPORTS and args.resume and should_skip_passports(cfg, log):
                results.append({"stage": stage, "status": "skipped", "duration": 0, "rc": 0})
                continue

            log.info("")
            log.info("─" * 60)
            log.info(f"▶ STAGE: {stage}")
            log.info("─" * 60)

            res = run_stage(stage, args, cfg, child_env, log)
            res["status"] = "ok" if res["ok"] else "failed"

            # Orchestration guard: the render stage exits 0 even when every SKU
            # times out (per-SKU errors are logged, not fatal). If it produced
            # zero raw PNGs the run is a silent failure — don't report success
            # or feed an empty input into the process stage.
            if res["ok"] and stage == STAGE_RENDER:
                raw_n = _count(get_path(cfg, "renders_raw"), "*.png")
                if raw_n == 0:
                    log.error("Render stage exited cleanly but produced 0 raw PNGs — treating as failure.")
                    res["ok"] = False
                    res["status"] = "failed"

            results.append(res)
            if not res["ok"]:
                log.error(f"Stage '{stage}' failed (rc={res['rc']}). Stopping pipeline "
                          f"(downstream stages skipped). Re-run with --resume after fixing.")
                aborted = True
    except KeyboardInterrupt:
        log.warning("Interrupted by user (Ctrl+C). Progress is saved; re-run with --resume to continue.")
        aborted = True

    total = time.time() - overall_start
    print_summary(results, artifact_counts(cfg), log_path, total, log)

    if any(r["status"] == "failed" for r in results):
        return 1
    if aborted:
        return 130
    return 0


if __name__ == "__main__":
    sys.exit(main())
