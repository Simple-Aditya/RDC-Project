# RDC-Project Research Handoff README

> **Purpose of this README:** This document is a full handoff guide for anyone continuing the RDC-Project dark pattern research. It explains what each dataset/code folder contains, how files relate to each other, and where to start depending on your task.

---

## 1) Project Overview

This repository appears to support a **dark patterns detection research pipeline** across:

1. Website source collection and scraping
2. Link/phrase sampling for annotation
3. Manual annotation and label preparation
4. ML model development and final training artifacts
5. Reference datasets and papers

Primary language in repository metadata is **Python (100%)**, with heavy use of CSV/XLSX data files.

Repository: `Simple-Aditya/RDC-Project`  
Default branch: `main`

---

## 2) Quick Start for New Researchers

If you are new and want to get productive fast:

1. Read this file fully.
2. Start with the high-level data inventory in Section 4.
3. Open these files first (in this order):
   - `Ecommerce Website Database (4).xlsx`
   - `Scraped Webpages Database.xlsx`
   - `Sampled Links for manual annotation.csv`
   - `Manual Annotation.csv`
   - `Final ML Labels and Files/` (folder)
4. Review code in:
   - `Website Scraper Code/`
   - `Dark Patterns ML Code/`
5. Validate schema assumptions (column names, IDs, URL keys) before running any new pipeline.

---

## 3) Repository Structure (Top-Level)

- `Dark Patterns Dataset.csv`
- `Dark Patterns ML Code/`
- `Ecommerce Website Database (4).xlsx`
- `Final ML Labels and Files/`
- `Manual Annotation.csv`
- `Mathur Dataset.csv`
- `Not Dark Patterns Dataset.csv`
- `Research Papers/`
- `Sampled Links Split in phrases.csv`
- `Sampled Links for manual annotation.csv`
- `Scraped Webpages Database.xlsx`
- `Website Scraper Code/`
- `README.md` (this file)

---

## 4) Data Inventory (What to Access and Where)

### A) Core Source/Collection Inputs

#### `Ecommerce Website Database (4).xlsx`
**Likely role:** Master/reference list of e-commerce websites and metadata used for scraping and study scope definition.  
**Use this when:**
- you need target domains/sites
- you need to expand or refresh scrape targets
- you need the original universe of websites

#### `Scraped Webpages Database.xlsx`
**Likely role:** Large raw/processed scrape output (largest file in repo) containing webpage-level collected data.  
**Use this when:**
- you need page text/content/source artifacts
- you need to regenerate sampling candidates
- you need traceability to extracted phrases or links

> Note: This is a very large file (~67 MB). Use chunked read workflows in Python if memory issues occur.

---

### B) Sampling and Annotation Pipeline Files

#### `Sampled Links for manual annotation.csv`
**Likely role:** Selected links/items intended for human annotation.  
**Use this when:**
- reproducing manual annotation set
- auditing what was sent to annotation
- creating new annotation batches

#### `Sampled Links Split in phrases.csv`
**Likely role:** Phrase-level transformed/split version of sampled links/pages, probably to support granular annotation and model features.  
**Use this when:**
- building phrase-level classifiers
- comparing link-level vs phrase-level labeling
- checking preprocessing quality

#### `Manual Annotation.csv`
**Likely role:** Human-labeled output used to create supervised ML labels.  
**Use this when:**
- training/evaluating supervised models
- quality-checking annotation consistency
- producing final train/val/test label files

---

### C) Derived / Final Modeling Datasets

#### `Dark Patterns Dataset.csv`
**Likely role:** Positive class dataset (dark-pattern examples).  
**Use this when:**
- binary classification setup
- positive class analysis
- balancing datasets

#### `Not Dark Patterns Dataset.csv`
**Likely role:** Negative class dataset (non-dark-pattern examples).  
**Use this when:**
- binary classification setup
- negative class baseline comparisons
- balancing and stratified sampling

#### `Final ML Labels and Files/`
**Likely role:** Final curated artifacts for modeling (clean labels, training-ready files, potentially splits/results).  
**Use this when:**
- you want stable inputs for model runs
- you want to avoid re-running full preprocessing
- you need the latest agreed label versions

---

### D) External/Reference Benchmark Data

#### `Mathur Dataset.csv`
**Likely role:** External/reference dataset (possibly from literature) for comparison or augmentation.  
**Use this when:**
- benchmarking against prior work
- transfer/generalization checks
- comparative taxonomy analysis

---

### E) Code Folders

#### `Website Scraper Code/`
**Likely role:** Python scripts/notebooks for scraping and extraction.  
**Use this when:**
- scraping new websites
- refreshing webpage data
- fixing scrape/parser logic

#### `Dark Patterns ML Code/`
**Likely role:** Python scripts/notebooks for training/evaluation/inference.  
**Use this when:**
- running model experiments
- hyperparameter tuning
- generating metrics/predictions

---

### F) Research Context

#### `Research Papers/`
**Likely role:** Supporting literature and background context used by the project.  
**Use this when:**
- understanding taxonomy/definitions
- writing reports or papers
- aligning labels/criteria with prior research

---

## 5) Recommended End-to-End Workflow

Use this flow when continuing the project:

1. **Target definition**
   - Start from `Ecommerce Website Database (4).xlsx`
2. **Scraping**
   - Run/update scripts in `Website Scraper Code/`
   - Save/update `Scraped Webpages Database.xlsx`
3. **Sampling**
   - Generate/refresh candidate sample files
   - Use `Sampled Links for manual annotation.csv`
   - Optionally generate phrase-level set: `Sampled Links Split in phrases.csv`
4. **Annotation**
   - Record labels in `Manual Annotation.csv`
5. **Label curation**
   - Build clean final labels and place in `Final ML Labels and Files/`
6. **Modeling**
   - Use `Dark Patterns ML Code/`
   - Train with positive/negative datasets and curated labels
7. **Evaluation and comparison**
   - Use `Mathur Dataset.csv` and internal final datasets for benchmarking

---

## 6) Data Linking Guidance (Critical for Continuity)

Because this project uses multiple datasets at different stages, continuity depends on preserving join keys.

When you continue, identify and preserve these kinds of keys (names may vary):
- URL / normalized URL
- Domain / hostname
- Website ID / source ID
- Scrape timestamp or batch ID
- Link ID / phrase ID
- Annotation item ID

### Minimum checks before any merge/join
- confirm key uniqueness in each dataset
- normalize URL format consistently (scheme, trailing slash, query handling)
- check duplicate rows before and after joins
- verify row count deltas are expected

---

## 7) Suggested Python Access Patterns

For large files and reproducibility:

- Prefer pandas with explicit dtype handling.
- Read large CSVs in chunks if needed.
- For XLSX files, document sheet names and selected columns in notebooks/scripts.

Example starter pattern:

```python
import pandas as pd

# CSV
df = pd.read_csv("Manual Annotation.csv")

# Large XLSX (specify sheet once known)
scrape_df = pd.read_excel("Scraped Webpages Database.xlsx", sheet_name=0)
```

If memory is tight:

```python
for chunk in pd.read_csv("Sampled Links Split in phrases.csv", chunksize=100000):
    # process chunk
    pass
```

---

## 8) Quality & Reproducibility Checklist

Before publishing results or handing off again:

- [ ] Document exact input files used (with file names and dates)
- [ ] Record code commit hash used for each experiment
- [ ] Save train/validation/test split logic and random seed
- [ ] Verify class distribution (dark vs non-dark)
- [ ] Verify no data leakage between splits
- [ ] Save model metrics and confusion matrices
- [ ] Save prediction outputs with source IDs/URLs for traceability

---

## 9) Risks / Things to Watch Out For

1. **Schema drift:** column names may differ between older/newer files.
2. **Label drift:** annotation criteria may evolve; keep decision rules documented.
3. **Duplicate data:** repeated URLs/pages can inflate metrics.
4. **Unclear provenance:** always track which stage generated each file.
5. **Large-file edits:** avoid manual edits in huge CSV/XLSX unless versioned carefully.

---

## 10) Handoff Notes for the Next Researcher

If you are taking over this work, do the following first week:

1. Create a small "data dictionary" markdown with exact column meanings for every core file.
2. Build a single pipeline map notebook/script that loads all major files and validates key joins.
3. Add a `requirements.txt` (if missing) based on actual imports from both code folders.
4. Create dated snapshots for any file you modify (especially annotation/label files).
5. Keep this README updated whenever file purpose or workflow changes.

---

## 11) If You Need to Extend the Research

Good next steps:
- expand website coverage in the ecommerce database
- improve phrase segmentation quality
- standardize annotation guidelines and inter-annotator checks
- add model explainability outputs (feature importances, error buckets)
- benchmark against additional external dark-pattern datasets

---

## 12) Maintainer Note

This README was written as a continuity handoff so future contributors can quickly locate data and understand the pipeline. If you change any dataset role or workflow stage, update this document immediately.
