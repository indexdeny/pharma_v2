# Ref migration report — completed 2026-11-18

The owner explicitly approved the exact five ref changes and their conditional order. GitHub repository identity and expected old refs were rechecked before execution. Master and both tags were replaced atomically using per-ref expected-old leases. A fresh master clone then passed runtime checks; default_branch was set to master and verified through API. Dev and backup were deleted atomically with their original exact leases after rechecking recovery, PR dependencies and protections.

| Ref | Initial object | Verified clean object/status |
|---|---|---|
| refs/heads/master | `cb61dd0be122b59b7fcf37f4c5d7fea04d67a2b8` | approved runtime baseline `48cfff2715f67c511092d9090fbb8c21df110adb`; subsequent reporting changes are fast-forward |
| refs/tags/v1.0.0 | `6ad92a61a7673aa9525f6aa47c7299e7607ce17f` | tag `e38320e221148e9a61547111ab8b16fc6d680f34`, commit `a08700b3c753dafc114005125d0ffe97b5927d55` |
| refs/tags/v1.0.1 | `d560b899c8af6422a236af76c85c2e940f347c26` | tag `30b5b54f5c643e00b78d8bf4b6c9dcd49bc36b90`, commit `6052d8f7f6df9c11cb67918ef0a0f7f64c998770` |
| refs/heads/backup/full-history-pre-v1.0 | `d24e0588e877663a117ed303dab616bb26a6ad92` | deleted |
| refs/heads/dev | `df31165cba41fe5155e63a9571417a89805a477d` | deleted |

Master is the sole public branch and the GitHub default. No private local-only refs or bundles were pushed. Both tags represent cleaned historical versions, not a new release; no GitHub Releases existed to migrate. The unrelated backup root was never merged. The necessary dev ancestry is preserved in the approved cleaned master.

Exact private recovery locations, full commit mappings, execution logs and backup hashes are retained by the owner. A fast-forward from old contaminated master could not remove its sensitive ancestors. Do not restore that old ancestry publicly. Cached objects and previous clones are outside public-ref reachability guarantees. [Final report](FINAL_PORTFOLIO_RELEASE_REPORT.md).
