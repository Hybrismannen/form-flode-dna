# GraceY Design Reference System

**System ID:** GY-DRS-1.0  
**Repository:** `Hybrismannen/form-flode-dna`  
**Status:** Active architecture / Pinterest ingestion staged  
**Initial source:** SRC-PIN-001

## 1. Function

GraceY Design Reference System (GY-DRS) converts external visual references into traceable design intelligence.

Its fundamental rule is:

> A reference is evidence of a useful visual relationship, not a template to copy.

The system therefore preserves provenance while extracting reusable structural principles.

## 2. Object model

### Layer A — Source

A platform, archive, board, site, collection or manually supplied corpus.

Examples: Pinterest boards, Behance collections, Dribbble, Are.na, Awwwards, official brand manuals, uploaded images.

### Layer B — Reference object

One specific Pin, project, page, image, interface, diagram or artifact.

Each object receives a stable `reference_id` and retains its original source URL and creator/source metadata whenever available.

### Layer C — Design DNA

A structured interpretation of the reference across:

- typography
- grid and layout
- hierarchy
- color logic
- geometry
- density
- imagery
- texture/materiality
- data-visualization language
- motion/interaction
- overall visual grammar
- reusable principles
- anti-patterns

### Layer D — Reference synthesis

Multiple Design-DNA objects can be clustered to identify:

- persistent Form & Flöde preferences
- emerging visual tendencies
- project-type patterns
- tensions or contradictions
- stylistic outliers
- reference families

### Layer E — Applied project rule

A project rule must name what is being transferred and what is not.

Example:

> Transfer the asymmetric information hierarchy and annotation density of references PIN-X and PIN-Y; do not transfer their palette. Apply the current RFSU brand palette and accessibility constraints.

## 3. Initial Pinterest binding

`SRC-PIN-001` is the canonical Pinterest board:

**Form & Flöde / Pius - Reference board**

The ingestion process:

1. obtains a short-lived Pinterest API token;
2. lists boards for the authenticated/developer account;
3. resolves the board by exact name;
4. retrieves every Pin with bookmark pagination;
5. records raw source metadata;
6. generates normalized GraceY reference objects;
7. updates source-sync metadata;
8. commits changes to the reference repository.

No Pinterest access token is stored in the repository.

## 4. Provenance and copyright boundary

GY-DRS separates analysis from asset possession.

By default:

- source identifiers are stored;
- original URLs are stored;
- creator/source information is preserved where available;
- remote image URLs may be stored as reference pointers;
- third-party binary creative assets are not mirrored into GitHub;
- derived analysis is stored locally in the corpus.

A project that needs licensed local assets must handle those assets through a separate rights-aware asset pipeline.

## 5. Downstream interfaces

The reference corpus is intended to feed:

### Figma
Design systems, UI composition, components, grids and visual implementation.

### Canva
Fast publication artifacts, social/presentation adaptation and brand-controlled composition.

### Miro / FigJam
Moodboards, synthesis maps, design-taxonomy maps and collaborative design reasoning.

### GitHub
Design tokens, implementation briefs, schemas, UI specifications and traceable project bindings.

### Pius / GraceY
Cross-project design reasoning and design-DNA synthesis.

## 6. Reference lifecycle

```
RAW-UNREVIEWED
      |
      v
REVIEWED
      |
      v
PRINCIPLE-EXTRACTED
      |
      +------> RETIRED
      |
      v
APPLIED
```

A reference can be retained without ever being applied. Application does not imply reproduction.

## 7. Immediate operational state

| Component | State |
|---|---|
| Canonical repository | ACTIVE |
| Reference schema | ACTIVE |
| Pinterest source registry | ACTIVE |
| Pinterest ingestion script | STAGED |
| GitHub scheduled sync | STAGED |
| Pinterest credentials | HUMAN ACTION REQUIRED |
| First corpus ingestion | BLOCKED ONLY BY CREDENTIALS |
| Design-DNA analysis | FOLLOWS FIRST INGESTION |

## 8. Human action boundary

The only external setup currently required is a Pinterest developer app tied to the source account and two repository secrets:

- `PINTEREST_APP_ID`
- `PINTEREST_APP_SECRET`

Once those secrets exist, the workflow can run without placing credentials in source control.
