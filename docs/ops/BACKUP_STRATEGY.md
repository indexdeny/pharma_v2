# Backup and recovery policy

Protect source catalogue/JSON inputs, non-reproducible render results and the agreed clean Git ref snapshot. Keep credentials and browser profiles outside repository archives intended for publication. Original contaminated history belongs only in restricted private recovery material.

A recovery check verifies archive hashes, restores objects in a separate repository, runs fsck and compares required source/data. Public rollback must use a verified clean point; do not restore an old contaminated ref. [Recovery policy](../../ROLLBACK_PLAN.md).
