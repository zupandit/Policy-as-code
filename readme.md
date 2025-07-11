# Policy-as-Code Dataset Generation

This repository documents the process of building a cleaned and enriched dataset of repositories using Policy as Code (PaC). The data was compiled from an initial set of GitHub repositories and enhanced with metadata such as commit history and popularity metrics.

## 📝 Workflow Overview

### 1. **Initial Data**
- `first.csv` and `repos.csv` were provided under the `init_data/` directory.
- These contained metadata and a list of ~500 GitHub repositories to analyze.

### 2. **Fetch GitHub Repo IDs**
- Script: `find_ids.py`
- Extracted GitHub repository IDs for all entries in `repos.csv`.

### 3. **Merge Initial Data**
- Merged `first.csv` with `repos_with_ids.csv` to form `combined.csv`.

### 4. **Row Normalization**
- Converted `combined.csv`, which had **multiple rows per repo**, into a **single row per repo** format using aggregation logic to produce `compiled.csv`.

### 5. **Collect First Commit Dates**
- Script: `repo_start.py`
- Fetched the **first commit date** for each repository using the GitHub API.

### 6. **Collect PaC File Introduced Dates**
- Also using `repo_start.py`, extracted the commit date when a PaC file (e.g., `.rego`, `.yaml`, etc.) was introduced.

### 7. **Fetch Last Commit Dates and Star Counts**
- Script: `last_commit.py`
- Fetched the latest commit timestamp and the star count for each repo.

### 8. **Data Cleaning**
- Manually reviewed the dataset:
  - Fixed 10 missing entries caused by connection/API issues.
  - Removed repos that were samples, examples, blueprints, or boilerplates (found during manual analysis).

### 9. **Final Dataset**
- Cleaned and consolidated into `final.csv`.
- Each row represents a unique repo with all relevant metadata.

---

## 📊 Analysis and Visualization

### Graphs
- Script: `graph.py`
- Generates various visualizations.

### Stats
- Script: `stats.py`
- Produces summary statistics.

---

## ✅ Output
- `final.csv`: Cleaned dataset with one row per repository.
- Graphs and statistics for research and publication purposes.


