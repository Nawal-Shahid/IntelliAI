<h1 align="center" style="background: linear-gradient(90deg, #6C63FF, #00B4D8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; font-size: 3em;">INTELLIAI</h1>

<h2 align="center" style="color:#2D3748; font-weight: 600;">Intelligent Data Analysis & Insights Platform</h2>

<p align="center">
  <img src="https://img.shields.io/badge/Language-Python-6C63FF?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/Framework-Streamlit-00B4D8?style=for-the-badge&logo=streamlit">
  <img src="https://img.shields.io/badge/Data%20Analysis-Pandas%20%7C%20NumPy-6C63FF?style=for-the-badge&logo=pandas">
  <img src="https://img.shields.io/badge/Visualization-Matplotlib%20%7C%20Seaborn-00B4D8?style=for-the-badge&logo=plotly">
  <img src="https://img.shields.io/badge/ML%20Engine-Groq%20AI-6C63FF?style=for-the-badge&logo=groq">
  <img src="https://img.shields.io/badge/License-MIT-00B4D8?style=for-the-badge&logo=open-source-initiative">
</p>

<p align="center">
  <a href="https://intelliai.streamlit.app" target="_blank">
    <img src="https://img.shields.io/badge/_Launch_App-6C63FF?style=for-the-badge&logo=streamlit&logoColor=white&labelColor=6C63FF&color=00B4D8&label=" alt="Launch App">
  </a>
</p>

<p align="center">
  <a href="https://github.com/Nawal-Shahid/IntelliAI">
    <img src="https://img.shields.io/github/stars/Nawal-Shahid/IntelliAI?style=social">
  </a>
  <a href="https://github.com/Nawal-Shahid/IntelliAI/issues">
    <img src="https://img.shields.io/github/issues/Nawal-Shahid/IntelliAI?style=social">
  </a>
  <a href="https://github.com/Nawal-Shahid/IntelliAI/forks">
    <img src="https://img.shields.io/github/forks/Nawal-Shahid/IntelliAI?style=social">
  </a>
</p>

---

**AI-Powered Self-Service Business Intelligence Platform**

IntelliAI is an end-to-end, AI-driven business intelligence platform built with Streamlit and powered by Groq's Llama 3.3 70B model. It transforms raw data into actionable insights through an intuitive 8-step workflow — no coding or data science expertise required.

---


## Application Overview
<div align="center">
<img width="1920" height="1080" alt="ezgif com-animated-gif-maker" src="https://github.com/user-attachments/assets/92f59868-7c1d-400d-b407-ced09eff5032" />
<br><br>



**Figure 1.** *IntelliAI's end-to-end analytics workflow demonstrating data ingestion, profiling, cleaning, exploratory analysis, visualization, AI-powered insights, conversational analytics, and report generation.*



</div>



---

## Features

### Complete Data Analysis Pipeline

| Step | Feature | Description |
|------|---------|-------------|
| 1 | **Data Upload** | Upload CSV or Excel files with automatic validation, encoding detection, delimiter auto-detection, and date parsing |
| 2 | **Data Profiling** | Automated analysis of dataset structure, column types, missing values, duplicates, outliers, and data quality scoring |
| 3 | **Data Cleaning** | Intelligent cleaning with missing value imputation (mean/median/mode), duplicate removal, outlier capping (IQR), and type conversion |
| 4 | **Exploratory Analysis** | Statistical summaries, distribution analysis (skewness/kurtosis), correlation matrices, and automated key insight extraction |
| 5 | **Interactive Dashboard** | Custom plotly visualizations (Bar, Line, Scatter, Pie, Histogram, Box) with AI-generated chart insights |
| 6 | **AI Insights** | Executive summaries, trend identification, anomaly detection, business recommendations, and risk analysis powered by Llama 3.3 70B |
| 7 | **Conversational AI** | Natural language Q&A about your data with context-aware responses and chat history |
| 8 | **Reports & Export** | Download cleaned data (CSV), executive summaries, and comprehensive analytics reports |

### AI Capabilities
- **Llama 3.3 70B** integration via Groq API for rapid inference
- **Visualization insights** — automatic interpretation of charts and graphs
- **Business analysis** — identifies trends, anomalies, correlations, and provides actionable recommendations
- **Natural language queries** — ask questions about your data conversationally
- **Context-aware responses** — adapts analysis based on dataset characteristics

### Data Quality
- Automated data type detection (numeric, categorical, datetime, text)
- Missing value analysis and handling
- Duplicate detection and removal
- Outlier detection via IQR method
- Correlation analysis with top positive/negative pair identification
- Overall quality scoring (0-100)

---

## System Requirements

- **Python**: 3.8+
- **Operating System**: Windows, macOS, or Linux
- **RAM**: 4GB minimum (8GB+ recommended for large datasets)
- **Storage**: 500MB for installation + dataset storage
- **Internet**: Required for AI features (Groq API)

---

## Installation

### 1. Clone or Download the Repository

```bash
git clone https://github.com/Nawal-Shahid/IntelliAI
cd IntelliAI
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Key

Create a `.env` file in the project root (or edit the existing one):

```env
GROQ_API_KEY=your_groq_api_key_here
```

> **Get your API key**: Visit [console.groq.com](https://console.groq.com) to sign up and obtain a free API key.

### 4. Run the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.

---

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `streamlit` | ≥1.28 | Web application framework |
| `pandas` | ≥1.5 | Data manipulation and analysis |
| `numpy` | ≥1.24 | Numerical computing |
| `plotly` | ≥5.17 | Interactive visualizations |
| `groq` | ≥0.4 | Groq API client for Llama 3.3 |
| `python-dotenv` | ≥1.0 | Environment variable management |
| `scikit-learn` | ≥1.3 | Data imputation utilities |
| `scipy` | ≥1.10 | Statistical analysis (skewness, kurtosis) |
| `openpyxl` | ≥3.1 | Excel file support |
| `chardet` | ≥5.2 | Character encoding detection |
| `python-multipart` | ≥0.0.6 | File upload handling |

Install all at once: `pip install -r requirements.txt`

---

## Usage Guide

### Quick Start

1. **Launch the app**: `streamlit run app.py`
2. **Upload data**: Click "Browse files" and select a CSV or Excel file
3. **Navigate steps**: Use the sidebar "Previous"/"Next" buttons or step indicators
4. **Run profiling**: Click "Run Profiling" to analyze data structure
5. **Clean data**: Configure cleaning options and apply
6. **Explore**: Run EDA, create visualizations, generate AI insights
7. **Chat**: Ask questions in natural language
8. **Export**: Download cleaned data and reports

### Workflow Steps

#### Step 1: Data Upload
- Supports CSV, .xlsx, .xls formats
- Auto-detects encoding (UTF-8, Latin-1, ISO-8859-1)
- Auto-detects CSV delimiters (comma, semicolon, tab, pipe)
- Validates file size (max 100MB), column count (1-500)
- Automatically converts date columns
- Cleans column names (strips whitespace, lowercase, underscores)

#### Step 2: Data Profiling
- Column-by-column type detection and statistics
- Missing value counts and percentages
- Duplicate row detection
- Data quality score (0-100)
- Automatic issue identification and recommendations

#### Step 3: Data Cleaning
- Missing value handling: Keep, Fill with mean/median/mode, or Drop rows
- Duplicate removal
- Outlier capping using IQR method (1.5× rule)
- Auto-convert data types (text to numeric when appropriate)

#### Step 4: Exploratory Data Analysis
- Descriptive statistics for all columns
- Distribution analysis (skewness, kurtosis, std deviation)
- Correlation matrix with heatmap styling
- Top positive/negative correlation identification
- Automated key insight extraction

#### Step 5: Interactive Dashboard
- **6 chart types**: Bar, Line, Scatter, Pie, Histogram, Box
- **Smart chart recommendations** based on data types
- **AI-generated insights** for each visualization
- Quick statistics panel
- Fully interactive plotly charts (zoom, pan, hover, export)

#### Step 6: AI-Powered Insights
- **Executive Summary**: High-level overview of what the data reveals
- **Trend Analysis**: Identifies 3-5 key patterns or trends
- **Anomaly Detection**: Flags outliers and concerning patterns
- **Business Recommendations**: 3-5 actionable recommendations
- **Risk Assessment**: Identifies potential risk factors
- Quick analysis buttons for key metrics and data quality assessment

#### Step 7: Conversational Analytics
- Natural language Q&A about your dataset
- Context-aware responses using column statistics
- Suggested questions for common analyses
- Chat history maintained during session

#### Step 8: Reports & Export
- Download cleaned dataset as CSV
- Generate and download executive summaries
- Comprehensive analytics report with expandable sections

---

## Project Structure

```
intelliAI/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (API key)
├── README.md                       # This file
└── modules/
    ├── __init__.py                 # Package init (optional)
    ├── data_ingestion.py           # File upload, validation, parsing
    ├── data_profiling.py           # Dataset profiling and quality scoring
    ├── data_cleaning.py            # Data cleaning and transformation
    ├── eda.py                      # Exploratory data analysis
    ├── visualization.py            # Chart generation and dashboards
    ├── insight_engine.py           # AI-powered business insights (Groq)
    └── conversational.py           # Natural language Q&A (Groq)
```

### Module Descriptions

| Module | Class | Responsibility |
|--------|-------|----------------|
| `data_ingestion.py` | `DataIngestion` | CSV/Excel loading, encoding detection, delimiter auto-detection, date conversion, validation |
| `data_profiling.py` | `DataProfiler` | Column analysis, type detection, missing value stats, quality scoring, issue identification |
| `data_cleaning.py` | `DataCleaner` | Missing value imputation, duplicate removal, outlier capping, type conversion, cleaning reports |
| `eda.py` | `ExploratoryDataAnalyzer` | Descriptive statistics, distribution analysis, correlation analysis, anomaly detection, insight extraction |
| `visualization.py` | `DashboardGenerator` | Chart recommendation, plotly chart creation (Bar, Line, Scatter, Pie, Histogram, Box), correlation heatmaps |
| `insight_engine.py` | `InsightEngine` | Groq LLM integration, business insight generation, visualization analysis, executive summaries, data quality assessment |
| `conversational.py` | `ConversationalAnalytics` | Natural language Q&A, context-aware responses, conversation history management |

---

## Theming

The application supports both **light** and **dark** modes automatically, adapting to your system's theme preference via Streamlit's built-in theme support.

**Theme Variables** (CSS custom properties):
- Backgrounds: Primary, secondary, card, metric, sidebar, chat bubbles
- Text: Primary, secondary, muted, on-primary, step indicators
- Borders: Generic, tabs, footer, step indicators
- Shadows: Cards, metrics
- Special: Badge colors (success/warning), insight card gradients, header gradient

---

## Configuration

### Environment Variables (`.env`)

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | Yes | Your Groq API key for LLM features |

### Streamlit Configuration (`.streamlit/config.toml` - optional)

```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f7f8fc"
textColor = "#2d3748"
font = "sans serif"

[server]
maxUploadSize = 200
```

### Data Cleaning Configuration

When using the Data Cleaning step, you can configure:
- **Missing Values**: Keep, Fill with mean, median, mode, or Drop rows
- **Duplicates**: Optionally remove duplicate rows
- **Outliers**: Optionally cap using IQR method (1.5× rule)
- **Type Conversion**: Auto-convert text columns to numeric when appropriate

---

## Limitations & Considerations

### File Size
- Maximum upload size: **200MB**
- For files >50MB, processing may be slower

### Data Types
- Maximum **500 columns**
- Minimum **1 column**
- Supported: Numeric, Categorical, Datetime, Text
- Datetime detection requires ≥80% successful conversion rate

### AI Features
- Requires internet connection
- Requires valid Groq API key
- AI responses may vary; verify critical insights
- Rate limits apply based on Groq API tier

### Performance
- Large datasets (>100K rows) may experience slower processing
- AI insights for large datasets may be truncated (1000 token limit)
- Correlation matrices limited to 10×10 for very wide datasets

---

## Privacy & Security

- **All data processing is local** — your data never leaves your machine
- **AI features use Groq API** — only dataset statistics and summaries are sent (not raw data)
- **No data persistence** — uploaded data exists only in memory during your session
- **Session reset** clears all data from memory

---

## Testing

To test the application with sample data:

```bash
# Create a sample CSV
python -c "
import pandas as pd
import numpy as np
np.random.seed(42)
df = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=100),
    'sales': np.random.normal(50000, 10000, 100),
    'customers': np.random.poisson(200, 100),
    'region': np.random.choice(['North', 'South', 'East', 'West'], 100),
    'product': np.random.choice(['A', 'B', 'C'], 100),
    'satisfaction': np.random.uniform(1, 5, 100)
})
df.to_csv('sample_data.csv', index=False)
print('Created sample_data.csv')
"
```

Then upload `sample_data.csv` to IntelliAI.

---

## Troubleshooting

### "No graph" / Visualization not showing
- Ensure data is loaded (Step 1 completed)
- Check that selected columns are appropriate for the chart type
- Try a different chart type (e.g., Bar Chart works with most data)
- For "Count" Y-axis, ensure X-axis has fewer than 1000 unique values

### "API key not found"
- Verify `.env` file exists in the project root
- Ensure `GROQ_API_KEY` is set and valid
- Restart the application after updating `.env`

### "Module not found" errors
- Run `pip install -r requirements.txt` to install all dependencies
- Ensure you're using Python 3.8+

### Slow performance
- Reduce dataset size (<100K rows recommended)
- Close other memory-intensive applications
- Use CSV instead of Excel for faster loading

---

## Contributing

Contributions are welcome! Please ensure:
1. Code follows existing patterns and style
2. All modules maintain backward compatibility
3. UI changes support both light and dark modes
4. CSS variables are used instead of hardcoded colors
5. Error handling is comprehensive

---

## License

This project is provided for educational and business use. The Groq API usage is subject to Groq's terms of service.

---

## Acknowledgments

- **Streamlit** for the incredible web framework
- **Groq** for the blazing-fast Llama 3.3 inference API
- **Plotly** for interactive visualization capabilities
- **Scikit-learn** for machine learning utilities
