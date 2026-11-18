# Repository classification

| Category | Policy |
|---|---|
| Runtime, shims, schemas and tests | Retain; no generation algorithm refactor |
| SSOT and 391 Stage 0 JSON passports | Retain original data |
| Optional CV Python helpers | Retain; dependencies/weights are not core runtime and are not exercised |
| Generated prompts, renders, progress and reports | Regenerate or restore privately; ignore in Git |
| Browser diagnostics, logs, historical archives and machine tooling | Exclude from public history; preserve privately |
| Source photos and pretrained weights | Withhold where third-party publication rights are unconfirmed |
| Demonstration | One real, source-traced generic preview |

[Cleanup policy](../CLEANUP_MANIFEST.md), [security](../FINAL_SECURITY_AUDIT.md).
