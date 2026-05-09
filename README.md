# Misdemeanors-in-Virginia-District-Courts-2010-2023
Interactive Streamlit dashboard for exploring misdemeanor caseflow, arrest patterns, and case dispositions in Virginia District Courts (2010–2023).

## Features

- Interactive Sankey diagram of caseflow
- Monthly charge trends over time
- Dynamic filtering by:
  - VCC Offense Category
  - VCC Specific Offense Type
  - Jurisdiction
- Summary tables with percentages
- Data pulled directly from GitHub

## Requirements
- Python 3.10+
- pip

## Installation

Clone the repository:
```bash
git clone https://github.com/brandmorrissey/Virginia_Misdemeanor_Caseflow.git
cd Virginia_Misdemeanor_Caseflow
```

Install required packages:
```bash
pip install -r requirements.txt
```

## Running the Dashboard
Run locally with Streamlit:

```bash
python -m streamlit run "Virginia_Misdemeanor_Caseflow.py"
```

## Data Source

Original court data were scraped from Virginia judicial records made available through [Virginia Court Data](https://virginiacourtdata.org/?utm_source=chatgpt.com).

The dashboard reads processed data directly from GitHub-hosted CSV files contained in this repository.
