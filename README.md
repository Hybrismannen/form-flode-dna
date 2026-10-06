# Form & Flöde DNA

Canonical visual-reference and design-DNA repository for Form & Flöde and the Pius/GraceY design layer.

## Purpose

This repository separates three things that must not be collapsed:

1. **Reference object** — an external work, Pin, page, image, project or other visual source.
2. **Extracted design principle** — the reusable visual/structural logic observed in the reference.
3. **Applied project rule** — a project-specific design decision derived from one or more principles.

The repository is therefore a design-intelligence layer, not an image scrapbook.

## First live source

**SRC-PIN-001 — Form & Flöde / Pius - Reference board**

Canonical board:
https://se.pinterest.com/linusfast/form-fl%C3%B6de-pius-reference-board/

Configuration:
`sources/pinterest/form-flode-pius-reference-board.json`

## Pipeline

```text
Pinterest / Behance / Dribbble / Are.na / Awwwards / other sources
        |
        v
Source Registry
        |
        v
Raw reference metadata
        |
        v
Design DNA extraction
        |
        v
GraceY reference corpus
        |
        +--> Figma
        +--> Canva
        +--> Miro / FigJam
        +--> GitHub implementations
        +--> project-specific briefs
```

## Pinterest sync

The workflow `.github/workflows/pinterest-reference-sync.yml` is staged for Pinterest API v5.

Required GitHub repository secrets:

- `PINTEREST_APP_ID`
- `PINTEREST_APP_SECRET`

The workflow remains a no-op until both are present. No Pinterest token is committed to this repository.

It requests a short-lived client-credentials token with `boards:read` and `pins:read`, resolves the configured board by exact board name, retrieves all Pins with pagination, normalizes their metadata and commits only the resulting reference metadata.

## Data policy

The repository does **not** mirror third-party creative works by default. It stores source identifiers, provenance, remote media URLs, metadata and derived design analysis. This keeps attribution and source traceability intact while allowing GraceY to reason over the reference corpus.

## Status

- Repository role: **canonical Form & Flöde visual-DNA/reference layer**
- GraceY binding: **active**
- Pinterest source: **registered**
- Automated Pinterest ingestion: **staged; credentials required**
- Design-DNA analysis: **schema active; analysis pass follows ingestion**

---

## Public provenance

<p align="left">
  <img src="https://raw.githubusercontent.com/Hybrismannen/form-flode-dna/main/assets/form-flode-logo.png" alt="Form & Flöde" width="120">
</p>

**Form & Flöde original public infrastructure.**  
Public provenance is governed by the **FFC Public Provenance Standard v1.0**.

### Support independent Form & Flöde work

Form & Flöde makes selected research, models, tools and development work openly available. If this work has been useful to you, you can support its continued development.

**[Support independent Form & Flöde work →](https://paypal.me/djlifehack)**
