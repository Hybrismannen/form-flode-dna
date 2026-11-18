# AI Google Drive Access & Privacy Rules — Director mandate

**Authority:** OAI-DRIVE-APPEND-ONLY-001 v1.0 (2026-11-18), privately stored in My Drive root / `0. Open AI - Access & Privacy Rules`.
**Exact source:** https://docs.google.com/document/d/18nexuzVfOEWwM7vXcPcB1NkjQHsEGKWxZHSqo-qlBRs/edit
**State:** Proposed repo adoption until approved and merged. Does not prove runtime enforcement.

**HARD DEFAULT DENY:** All already-existing Google Drive files, folders, contents, revisions, metadata, permissions and trash state are immutable to AI unless the Director explicitly approves the exact target IDs, proposed action, scope and consequence BEFORE execution. No edit, overwrite, rename, move, replace, re-share, permission change, deletion, trash, purge, deduplication, bulk sync, cleanup, rollback or automatic temporary-file removal without approval. A generic project instruction, broad OAuth access or past approval is NOT permission. On uncertainty, fail closed.

**ALLOW:** Read task-relevant files; create genuinely NEW, private files/folders in authorized destinations, initialize their content as part of the initial creation transaction and verify. New items become protected after creation. No data exfiltration or public sharing.

**Required operational integration:** read authoritative policy before Drive tasks; pre-effect action classification; server-side policy gate before EVERY Drive mutation; itemized Director approval bound to immutable file ID and effect; deny if approval/policy unavailable, logging/pre-effect and post-effect evidence; negative tests for edit/delete/trash/move/overwrite/permission changes/bulk-sync bypass. No system may self-authorize, and a Markdown reference alone is not enforcement.

Preserve current CDX, Pius, FFC/FFOS, AMA and existing repo release/constitutional protocols. No existing repo artifact or historical baseline is altered by this proposal.
