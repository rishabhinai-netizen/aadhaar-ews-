# Aadhaar Early Warning System (EWS)

This project presents a national-level Early Warning System (EWS) for Aadhaar
enrolment and update monitoring. The system uses weekly, PIN-validated,
district-level aggregates to detect emerging service delivery risks.

## Key Features
- Trend-based early warning (not just spikes)
- PIN-code based geospatial canonicalisation
- District-level risk ranking
- Interactive Streamlit dashboard
- Privacy-preserving (aggregated data only)

## Data Sources
- Aadhaar Enrolment (aggregated)
- Aadhaar Demographic Updates (aggregated)
- Aadhaar Biometric Updates (aggregated)
- Government of India PIN directory (for geo validation)

## How to Run
```bash
pip install -r requirements.txt
streamlit run app.py
