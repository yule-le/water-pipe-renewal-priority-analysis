# water-pipe-renewal-priority-analysis

## Project Overview

This is a lightweight portfolio project that uses open water pipe asset data to assess data quality, understand the current pipe asset profile, and create a simple renewal priority screening list.

The project is designed to produce clear, business-friendly outputs rather than a complex technical system. It supports portfolio-level asset review by combining basic data checks, descriptive analysis, and a transparent screening approach.

This project provides a portfolio-level screening approach, not a pipe failure prediction model or engineering assessment.

## Business Context

Water utilities often manage aging underground pipe networks with incomplete asset records and limited renewal budgets. A practical first step is to understand what asset data is available, where the main data quality gaps are, and which assets may warrant closer review for future renewal planning.

This repository demonstrates a simple analyst workflow for that purpose using open water pipe asset data.

## Project Outputs

The repository is intended to support three lightweight outputs:

- A business-friendly markdown report
- A notebook that documents the analysis workflow
- Exported charts and summary tables for screening results

Large row-level files such as the raw source dataset, the cleaned full asset table, and the full priority export are generated locally but not committed in this public portfolio version.

## Repository Structure

```text
water-pipe-renewal-priority-analysis/
|-- README.md
|-- asset_renewal_priority_report.md
|-- analysis/
|   `-- water_pipe_analysis.ipynb
|-- data/
|   `-- raw/
|       `-- README.md
|-- outputs/
|   |-- charts/
|   `-- tables/
|-- requirements.txt
`-- .gitignore
```

## How to Run

1. Create and activate a Python environment.
2. Install dependencies from `requirements.txt`.
3. Place raw input files in `data/raw/`.
4. Open `analysis/water_pipe_analysis.ipynb` in Jupyter.
5. Run the notebook sections step by step to generate charts, tables, and the screening output list.

For GitHub presentation, the repository keeps report-ready charts and summary tables in version control, while larger row-level outputs remain local.

## Limitations

- The project depends on the quality and completeness of the available open asset data.
- The screening logic is intended for portfolio review and prioritisation support only.
- The outputs do not predict pipe failures or determine final renewal decisions.
- More detailed engineering review would still be required before any operational or capital planning decision.
- Public repository contents are intentionally lighter than the full local working files to keep the portfolio version readable and easier to clone.
