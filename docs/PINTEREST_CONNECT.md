# Pinterest connection — activation checklist

**Target source:** SRC-PIN-001  
**Board:** Form & Flöde / Pius - Reference board  
**Mode:** Pinterest API v5 / client credentials

The repository implementation is complete. This checklist activates it.

## 1. Pinterest developer app

Use the Pinterest developer account associated with the Pinterest account that owns the reference board.

Create or select an app in Pinterest **My apps** and confirm the app has access to API v5.

Client-credentials grants require two-factor authentication for the app/account.

## 2. Credentials

From the Pinterest app configuration, obtain:

- App ID
- App secret

Do **not** paste either credential into repository files, issues, commits or chat logs intended for publication.

## 3. GitHub repository secrets

In:

`Hybrismannen/form-flode-dna`

open:

`Settings → Secrets and variables → Actions → New repository secret`

Create exactly:

- `PINTEREST_APP_ID` = Pinterest App ID
- `PINTEREST_APP_SECRET` = Pinterest App secret

The workflow already reads these names.

## 4. First run

Open:

`Actions → Pinterest reference sync → Run workflow`

Expected sequence:

1. GitHub requests a short-lived Pinterest client-credentials token.
2. The integration lists the authenticated/developer account's boards.
3. It resolves `Form & Flöde / Pius - Reference board` by exact name.
4. It retrieves all Pins with API pagination.
5. It writes:
   - `data/pinterest/form-flode-pius-reference-board/raw.json`
   - `data/pinterest/form-flode-pius-reference-board/normalized.json`
6. The source registry is updated with the Pinterest board ID and sync timestamp.
7. GitHub Actions commits the updated metadata.

## 5. Automatic operation

After a successful first run, the workflow is scheduled daily.

No long-lived Pinterest access token is stored. A new short-lived token is requested from the app credentials on each run.

## 6. Failure interpretation

### 401 / authentication failure
Check the App ID, App secret, 2FA requirement and app status.

### 403 / PINNER_DATA_ACCESS_DENIED
For a board owned by the same account attached to the app, verify that the token/app is actually operating as that account and that the necessary API access tier is active. Do not loop retries.

### Board not found
The script deliberately requires an exact board-name match. Either restore the canonical board name or set a repository/workflow environment override for `PINTEREST_BOARD_ID`.

## 7. Security boundary

The public repository may contain:

- source URLs
- Pin IDs
- board IDs
- creator/source metadata
- remote media URLs
- derived Design-DNA analysis

It must never contain:

- App secret
- access tokens
- authentication headers
- private/secret-board data unless the repository is first moved behind an appropriate access boundary
