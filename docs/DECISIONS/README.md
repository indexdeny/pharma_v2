# Architecture Decision Records (ADR)

Each ADR captures **one significant technical decision** and *why* it was made,
so the reasoning survives the author. Format: Context → Decision → Consequences →
Alternatives. Status values: `Accepted`, `Superseded`, `Deprecated`.

> Some rationale was reconstructed from the code and git history during the
> Production Hardening phase and is marked **[confirm with author]** where it
> could not be fully grounded in the repository.

| ADR | Decision | Status |
|---|---|---|
| [ADR-001](ADR-001-why-gemini.md) | Google Gemini as the image generator | Accepted |
| [ADR-002](ADR-002-why-markdown.md) | Markdown as the passport/prompt format | Accepted |
| [ADR-003](ADR-003-why-webp.md) | WEBP (1600×1600, ≤500 KB) as the final asset format | Accepted |
| [ADR-004](ADR-004-why-rpa.md) | Selenium RPA (browser) instead of an image API | Accepted |
| [ADR-005](ADR-005-ssot-routing-authority.md) | `SSOT/SKU.csv` as the primary routing authority | Accepted |
| [ADR-006](ADR-006-unified-entrypoint.md) | Unified `main.py` + subprocess orchestration | Accepted |
