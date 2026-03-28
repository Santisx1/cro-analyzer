# CRO Analysis Project - Copilot Instructions

## Project Overview
Automated CRO (Conversion Rate Optimization) analysis tool that integrates with Google Analytics and heatmap data to provide conversion funnel analysis and optimization recommendations.

## Technology Stack
- **Language**: Python 3.10+
- **Main Libraries**: pandas, numpy, matplotlib, plotly
- **APIs**: Google Analytics 4
- **Data Format**: JSON, CSV

## Key Features
1. Automated funnel analysis from GA4 data
2. Heatmap integration (Microsoft Clarity, Hotjar)
3. Abandonment point detection
4. Automated optimization recommendations
5. HTML/PDF report generation
6. Batch processing capability

## Project Structure
```
├── src/
│   ├── __init__.py
│   ├── analyzer.py          # Main CRO analysis engine
│   ├── data_processor.py    # GA4 and heatmap data processing
│   ├── recommendations.py   # AI-powered recommendations
│   ├── reports.py           # Report generation (HTML/PDF)
│   └── integrations/
│       ├── __init__.py
│       ├── google_analytics.py
│       └── heatmap_provider.py
├── tests/
│   ├── __init__.py
│   ├── test_analyzer.py
│   ├── test_data_processor.py
│   └── test_recommendations.py
├── examples/
│   ├── sample_config.json
│   └── sample_data.csv
├── requirements.txt
├── README.md
└── main.py
```

## Configuration
- Credentials stored in `config.json` (user-provided)
- Sample configuration in `examples/sample_config.json`

## Development Notes
- Use virtual environment for dependency isolation
- Follow PEP 8 style guidelines
- Add unit tests for new features
- Data processing optimized for datasets up to 1M rows
