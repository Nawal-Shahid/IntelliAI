import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os
from dotenv import load_dotenv
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import re

# Load environment variables
load_dotenv()

# Add modules to path
sys.path.append(str(Path(__file__).parent))

from modules.data_ingestion import DataIngestion
from modules.data_profiling import DataProfiler
from modules.data_cleaning import DataCleaner
from modules.eda import ExploratoryDataAnalyzer
from modules.visualization import DashboardGenerator
from modules.insight_engine import InsightEngine
from modules.conversational import ConversationalAnalytics

# Page configuration
st.set_page_config(
    page_title="IntelliAI - Business Intelligence Platform",
    page_icon="https://cdn-icons-png.flaticon.com/512/8932/8932269.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

def render_ai_content(text):
    """Convert markdown bold/italic from LLM to HTML for rendering in cards"""
    if not text:
        return text
    # Convert **bold** to <strong>bold</strong>
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Convert *italic* to <em>italic</em> (but not inside <strong>)
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', text)
    # Convert newlines to <br>
    text = text.replace('\n', '<br>')
    return text

# Custom CSS for beautiful UI - works in both dark and light mode
st.markdown("""
<style>
    /* CSS Variables for theming - Light mode defaults */
    :root, [data-theme="light"] {
        --bg-primary: #ffffff;
        --bg-secondary: #f7f8fc;
        --bg-card: #ffffff;
        --bg-metric: #ffffff;
        --bg-insight: linear-gradient(135deg, #f8f9ff 0%, #f0e6ff 100%);
        --bg-step-completed: #f0fff4;
        --bg-step-current: linear-gradient(135deg, #f8f9ff 0%, #f0e6ff 100%);
        --bg-chat-user: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --bg-chat-bot: #f0f2f6;
        --bg-badge-success: linear-gradient(135deg, #f0fff4 0%, #e6fffa 100%);
        --bg-badge-warning: linear-gradient(135deg, #fffff0 0%, #feffe6 100%);
        --text-primary: #2d3748;
        --text-secondary: #4a5568;
        --text-muted: #718096;
        --text-on-primary: #ffffff;
        --text-step-completed: #22543d;
        --text-step-current: #553c7b;
        --text-step-pending: #718096;
        --border-color: #e2e8f0;
        --border-step-completed: #48bb78;
        --border-step-current: #667eea;
        --shadow-card: 0 2px 8px rgba(0,0,0,0.06);
        --shadow-metric: 0 2px 4px rgba(0,0,0,0.04);
        --sidebar-bg: #f7f8fc;
        --footer-border: #e2e8f0;
        --tabs-border: #e2e8f0;
        --chat-bot-border: #e8e8e8;
        --alert-text: #2d3748;
        --input-bg: #ffffff;
        --heading-color: #2d3748;
        --strong-insight: #553c7b;
        --em-insight: #667eea;
    }

    /* Dark mode overrides */
    [data-theme="dark"] {
        --bg-primary: #1a1a2e;
        --bg-secondary: #16213e;
        --bg-card: #1e293b;
        --bg-metric: #1e293b;
        --bg-insight: linear-gradient(135deg, #1a1a2e 0%, #1e293b 100%);
        --bg-step-completed: #0f4c3a;
        --bg-step-current: linear-gradient(135deg, #1a1a2e 0%, #2d1b69 100%);
        --bg-chat-user: linear-gradient(135deg, #5a6fd6 0%, #6a3da0 100%);
        --bg-chat-bot: #1e293b;
        --bg-badge-success: linear-gradient(135deg, #0f4c3a 0%, #0a3d31 100%);
        --bg-badge-warning: linear-gradient(135deg, #4a3f0a 0%, #3d3508 100%);
        --text-primary: #e2e8f0;
        --text-secondary: #a0aec0;
        --text-muted: #718096;
        --text-on-primary: #ffffff;
        --text-step-completed: #68d391;
        --text-step-current: #a78bfa;
        --text-step-pending: #718096;
        --border-color: #2d3748;
        --border-step-completed: #48bb78;
        --border-step-current: #667eea;
        --shadow-card: 0 2px 8px rgba(0,0,0,0.2);
        --shadow-metric: 0 2px 4px rgba(0,0,0,0.15);
        --sidebar-bg: #16213e;
        --footer-border: #2d3748;
        --tabs-border: #2d3748;
        --chat-bot-border: #2d3748;
        --alert-text: #e2e8f0;
        --input-bg: #1e293b;
        --heading-color: #e2e8f0;
        --strong-insight: #a78bfa;
        --em-insight: #93c5fd;
    }

    /* Main container styling */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 16px;
        color: #ffffff !important;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .main-header h1 {
        font-size: 2.8rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        color: #ffffff !important;
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.95;
        font-weight: 300;
        color: #ffffff !important;
    }
    
    /* Card styling */
    .card {
        background-color: var(--bg-card);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: var(--shadow-card);
        margin-bottom: 1rem;
        border: 1px solid var(--border-color);
        color: var(--text-primary);
    }
    
    .card h3 {
        color: var(--heading-color);
        margin-top: 0;
        margin-bottom: 0.8rem;
    }
    
    .card ul {
        color: var(--text-secondary);
        line-height: 1.6;
        padding-left: 1.2rem;
    }
    
    .insight-card {
        background: var(--bg-insight);
        padding: 1.2rem 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        font-size: 0.95rem;
        line-height: 1.7;
        color: var(--text-primary);
    }
    
    .insight-card strong {
        color: var(--strong-insight);
    }
    
    .insight-card em {
        color: var(--em-insight);
    }
    
    .metric-card {
        background: var(--bg-metric);
        padding: 1.2rem;
        border-radius: 12px;
        text-align: center;
        border: 1px solid var(--border-color);
        transition: transform 0.2s, box-shadow 0.2s;
        box-shadow: var(--shadow-metric);
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);
        border-color: #667eea;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: var(--text-secondary);
        margin-top: 0.3rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border: none;
        padding: 0.6rem 1.8rem;
        border-radius: 10px;
        font-weight: 500;
        transition: all 0.3s;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.25);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Secondary button */
    .stButton > button[kind="secondary"] {
        background: transparent;
        color: #667eea !important;
        border: 2px solid #667eea;
        box-shadow: none;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: var(--sidebar-bg);
    }
    
    .sidebar-header {
        padding: 1.2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border-radius: 12px;
        margin-bottom: 1.2rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
    }
    
    .sidebar-header h3 {
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0;
        color: #ffffff !important;
    }
    
    /* Progress step styling */
    .step-completed {
        color: var(--text-step-completed);
        font-weight: 600;
        padding: 0.6rem 0.8rem;
        border-left: 3px solid var(--border-step-completed);
        margin: 0.4rem 0;
        background-color: var(--bg-step-completed);
        border-radius: 0 8px 8px 0;
        font-size: 0.9rem;
    }
    
    .step-current {
        color: var(--text-step-current);
        font-weight: 600;
        padding: 0.6rem 0.8rem;
        border-left: 3px solid var(--border-step-current);
        margin: 0.4rem 0;
        background: var(--bg-step-current);
        border-radius: 0 8px 8px 0;
        font-size: 0.9rem;
    }
    
    .step-pending {
        color: var(--text-step-pending);
        padding: 0.6rem 0.8rem;
        margin: 0.4rem 0;
        font-size: 0.9rem;
    }
    
    /* Data table styling */
    .dataframe {
        font-size: 0.9rem;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: var(--text-muted);
        font-size: 0.8rem;
        border-top: 1px solid var(--footer-border);
        margin-top: 2rem;
    }
    
    /* Status badges */
    .badge-success {
        background: var(--bg-badge-success);
        color: var(--text-step-completed);
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        border: 1px solid #c6f6d5;
    }
    
    .badge-warning {
        background: var(--bg-badge-warning);
        color: #d69e2e;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        border: 1px solid #fefcbf;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        border-bottom: 2px solid var(--tabs-border);
    }
    
    .stTabs [data-baseweb="tab"] {
        font-size: 1rem;
        font-weight: 500;
        color: var(--text-secondary);
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #667eea;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: var(--heading-color);
        font-weight: 600;
    }
    
    h2 {
        font-size: 1.5rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid var(--border-color);
        padding-bottom: 0.5rem;
    }
    
    /* Success/Error/Info messages - improve contrast */
    .stAlert {
        border-radius: 10px;
        border: none;
    }
    
    .stAlert > div {
        color: var(--alert-text) !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        font-weight: 500;
        color: var(--text-primary) !important;
    }
    
    /* Fix text input contrast */
    .stTextInput input {
        color: var(--text-primary) !important;
        background-color: var(--input-bg) !important;
    }
    
    /* Fix select box contrast */
    .stSelectbox div[data-baseweb="select"] {
        color: var(--text-primary) !important;
    }
    
    /* Fix caption contrast */
    .stCaption {
        color: var(--text-secondary) !important;
    }
    
    /* Fix metric text contrast */
    [data-testid="stMetricValue"] {
        color: var(--text-primary) !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: var(--text-secondary) !important;
    }
    
    /* Fix spinner text */
    .stSpinner > div {
        color: var(--text-secondary) !important;
    }
    
    /* Fix file uploader text */
    .stFileUploader label {
        color: var(--text-primary) !important;
    }
    
    /* Fix checkbox label */
    .stCheckbox label {
        color: var(--text-primary) !important;
    }
    
    /* Ensure sidebar text is readable */
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label {
        color: var(--text-primary) !important;
    }
    
    /* Markdown text in dark mode */
    [data-theme="dark"] .stMarkdown p,
    [data-theme="dark"] .stMarkdown li,
    [data-theme="dark"] .stMarkdown span:not([class]) {
        color: var(--text-primary);
    }
    
    /* DataFrame styling in dark mode */
    [data-theme="dark"] .dataframe {
        color: var(--text-primary);
    }
    
    /* Info/warning/error box text in dark mode */
    [data-theme="dark"] div[data-testid="stInfo"] *,
    [data-theme="dark"] div[data-testid="stWarning"] *,
    [data-theme="dark"] div[data-testid="stError"] *,
    [data-theme="dark"] div[data-testid="stSuccess"] * {
        color: var(--alert-text) !important;
    }
    
    /* Select box dropdown in dark mode */
    [data-theme="dark"] div[data-baseweb="select"] > div {
        background-color: var(--input-bg) !important;
    }
    
    /* Text area in dark mode */
    [data-theme="dark"] textarea {
        color: var(--text-primary) !important;
        background-color: var(--input-bg) !important;
    }
    
    /* Number input in dark mode */
    [data-theme="dark"] input[type="number"] {
        color: var(--text-primary) !important;
        background-color: var(--input-bg) !important;
    }
    
    /* Sidebar select boxes in dark mode */
    [data-theme="dark"] section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: var(--input-bg) !important;
    }
    
    /* Sidebar text in dark mode */
    [data-theme="dark"] section[data-testid="stSidebar"] .stMarkdown p,
    [data-theme="dark"] section[data-testid="stSidebar"] .stMarkdown span {
        color: var(--text-primary) !important;
    }
    
    /* Expander content in dark mode */
    [data-theme="dark"] .streamlit-expanderContent {
        color: var(--text-primary);
    }
</style>
""", unsafe_allow_html=True)

class IntelliAI:
    def __init__(self):
        self.initialize_session_state()
        self.data_ingestion = DataIngestion()
        self.data_profiler = DataProfiler()
        self.data_cleaner = DataCleaner()
        self.eda_analyzer = ExploratoryDataAnalyzer()
        self.dashboard_generator = DashboardGenerator()
        self.insight_engine = InsightEngine()
        self.conversational_analytics = ConversationalAnalytics()
    
    def initialize_session_state(self):
        """Initialize all session state variables"""
        if 'data' not in st.session_state:
            st.session_state.data = None
        if 'cleaned_data' not in st.session_state:
            st.session_state.cleaned_data = None
        if 'profile_report' not in st.session_state:
            st.session_state.profile_report = None
        if 'current_step' not in st.session_state:
            st.session_state.current_step = 1
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        if 'cleaning_done' not in st.session_state:
            st.session_state.cleaning_done = False
        if 'eda_results' not in st.session_state:
            st.session_state.eda_results = None
        if 'dashboard_fig' not in st.session_state:
            st.session_state.dashboard_fig = None
        if 'dashboard_insight' not in st.session_state:
            st.session_state.dashboard_insight = None
    
    def render_header(self):
        """Render the main header"""
        st.markdown("""
        <div class="main-header">
            <h1>IntelliAI</h1>
            <p>AI-Powered Self-Service Business Intelligence Platform</p>
            <p style="font-size: 0.9rem; opacity: 0.9;">Transform raw data into actionable insights</p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_sidebar(self):
        """Render sidebar with workflow progress"""
        with st.sidebar:
            st.markdown('<div class="sidebar-header"><h3>Workflow Progress</h3></div>', unsafe_allow_html=True)
            
            steps = {
                1: "Data Upload",
                2: "Data Profiling", 
                3: "Data Cleaning",
                4: "Exploratory Analysis",
                5: "Dashboard",
                6: "AI Insights",
                7: "Conversational AI",
                8: "Reports"
            }
            
            for step_num, step_name in steps.items():
                if step_num < st.session_state.current_step:
                    st.markdown(f'<div class="step-completed">&#10003; {step_name}</div>', unsafe_allow_html=True)
                elif step_num == st.session_state.current_step:
                    st.markdown(f'<div class="step-current">&#9654; {step_name}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="step-pending">{step_name}</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Navigation
            st.markdown("### Navigation")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Previous", disabled=st.session_state.current_step == 1):
                    if st.session_state.current_step > 1:
                        st.session_state.current_step -= 1
                        st.rerun()
            
            with col2:
                if st.button("Next", disabled=st.session_state.current_step == 8):
                    if self.can_proceed_to_next():
                        st.session_state.current_step += 1
                        st.rerun()
            
            st.markdown("---")
            
            # Dataset Status
            st.markdown("### Dataset Status")
            if st.session_state.data is not None:
                status_color = "badge-success"
                status_text = "Loaded"
            else:
                status_color = "badge-warning"
                status_text = "Not Loaded"
            
            st.markdown(f'<span class="{status_color}">{status_text}</span>', unsafe_allow_html=True)
            
            if st.session_state.data is not None:
                st.caption(f"Rows: {len(st.session_state.data):,}")
                st.caption(f"Columns: {len(st.session_state.data.columns)}")
            
            st.markdown("---")
            
            # Reset button
            if st.button("Reset Application", type="secondary"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
    
    def can_proceed_to_next(self):
        """Check if we can proceed to next step"""
        current = st.session_state.current_step
        
        if current == 1 and st.session_state.data is None:
            st.error("Please upload data first")
            return False
        elif current == 2 and st.session_state.data is None:
            st.error("No data available")
            return False
        elif current == 3 and st.session_state.data is None:
            st.error("No data available")
            return False
        elif current == 4 and st.session_state.cleaned_data is None and st.session_state.data is None:
            st.error("No data available")
            return False
        
        return True
    
    def data_upload_step(self):
        """Step 1: Data Upload and Ingestion"""
        st.header("Data Upload and Ingestion")
        st.markdown("Upload your dataset to begin the analysis workflow.")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            uploaded_file = st.file_uploader(
                "Choose a file",
                type=['csv', 'xlsx', 'xls'],
                help="Supported formats: CSV, Excel (.xlsx, .xls)",
                key="file_uploader"
            )
            
            if uploaded_file and st.session_state.data is None:
                with st.spinner("Loading and validating dataset..."):
                    df, success, message = self.data_ingestion.ingest(uploaded_file)
                    
                    if success:
                        st.session_state.data = df
                        st.success(f"Success: {message}")
                        st.rerun()
                    else:
                        st.error(f"Error: {message}")
            
            if st.session_state.data is not None:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader("Dataset Overview")
                
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.markdown(f'<div class="metric-card"><div class="metric-value">{len(st.session_state.data):,}</div><div class="metric-label">Total Rows</div></div>', unsafe_allow_html=True)
                with col_b:
                    st.markdown(f'<div class="metric-card"><div class="metric-value">{len(st.session_state.data.columns)}</div><div class="metric-label">Total Columns</div></div>', unsafe_allow_html=True)
                with col_c:
                    memory_mb = st.session_state.data.memory_usage(deep=True).sum() / 1024**2
                    st.markdown(f'<div class="metric-card"><div class="metric-value">{memory_mb:.1f}</div><div class="metric-label">Memory (MB)</div></div>', unsafe_allow_html=True)
                
                st.subheader("Data Preview")
                st.dataframe(st.session_state.data.head(10), use_container_width=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="card">
                <h3>Supported Formats</h3>
                <ul>
                    <li>Excel files (.xlsx, .xls)</li>
                    <li>CSV files</li>
                    <li>Auto-validation included</li>
                    <li>Type detection</li>
                    <li>Date parsing</li>
                </ul>
                <h3>File Requirements</h3>
                <ul>
                    <li>Maximum size: 100MB</li>
                    <li>Minimum 1 column</li>
                    <li>Maximum 500 columns</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    def data_profiling_step(self):
        """Step 2: Automated Data Profiling"""
        st.header("Data Profiling")
        st.markdown("Analyze dataset structure, quality, and characteristics.")
        
        if st.session_state.data is not None:
            if st.session_state.profile_report is None:
                if st.button("Run Profiling", type="primary"):
                    with st.spinner("Analyzing dataset..."):
                        profile = self.data_profiler.generate_profile(st.session_state.data)
                        st.session_state.profile_report = profile
                    st.rerun()
            
            if st.session_state.profile_report is not None:
                profile = st.session_state.profile_report
                
                # Summary metrics
                col1, col2, col3, col4 = st.columns(4)
                total_records = profile.get('total_records', 0)
                total_columns = profile.get('total_columns', 0)
                
                with col1:
                    st.markdown(f'<div class="metric-card"><div class="metric-value">{total_records:,}</div><div class="metric-label">Total Records</div></div>', unsafe_allow_html=True)
                with col2:
                    st.markdown(f'<div class="metric-card"><div class="metric-value">{total_columns}</div><div class="metric-label">Total Attributes</div></div>', unsafe_allow_html=True)
                with col3:
                    total_cells = total_records * total_columns
                    missing_total = profile.get('missing_values', {}).get('total', 0)
                    missing_pct = (missing_total / total_cells * 100) if total_cells > 0 else 0
                    st.markdown(f'<div class="metric-card"><div class="metric-value">{missing_pct:.1f}%</div><div class="metric-label">Missing Values</div></div>', unsafe_allow_html=True)
                with col4:
                    st.markdown(f'<div class="metric-card"><div class="metric-value">{profile.get("duplicates", 0):,}</div><div class="metric-label">Duplicate Rows</div></div>', unsafe_allow_html=True)
                
                # Column analysis
                st.subheader("Column Analysis")
                col_data = []
                for col, info in profile.get('column_types', {}).items():
                    col_data.append({
                        'Column': col,
                        'Type': info.get('detected_type', 'unknown').capitalize(),
                        'Unique Values': info.get('unique_count', 0),
                        'Missing': profile.get('missing_values', {}).get('by_column', {}).get(col, 0),
                        'Missing %': f"{(profile.get('missing_values', {}).get('by_column', {}).get(col, 0) / total_records * 100) if total_records > 0 else 0:.1f}%"
                    })
                
                st.dataframe(pd.DataFrame(col_data), use_container_width=True)
                
                # Quality score
                quality_score = self.data_profiler.quality_score(st.session_state.data)
                st.subheader("Data Quality Score")
                st.progress(quality_score / 100)
                st.caption(f"Overall Score: {quality_score}/100")
                
                # Issues and recommendations
                col1, col2 = st.columns(2)
                with col1:
                    if profile.get('issues'):
                        st.warning("Issues Detected")
                        for issue in profile['issues'][:5]:
                            st.write(f"• {issue}")
                
                with col2:
                    if profile.get('recommendations'):
                        st.info("Recommendations")
                        for rec in profile['recommendations'][:5]:
                            st.write(f"• {rec}")
                
                if st.button("Re-run Profiling"):
                    st.session_state.profile_report = None
                    st.rerun()
        
        else:
            st.warning("Please upload data in Step 1 first")
    
    def data_cleaning_step(self):
        """Step 3: Intelligent Data Cleaning"""
        st.header("Data Cleaning")
        st.markdown("Clean and prepare your data for analysis.")
        
        if st.session_state.data is not None:
            data_to_clean = st.session_state.cleaned_data if st.session_state.cleaned_data is not None else st.session_state.data
            
            # Cleaning status
            if st.session_state.cleaned_data is not None:
                st.success(f"Data has been cleaned. Current dataset has {len(st.session_state.cleaned_data):,} rows.")
                if st.button("Reclean Original Data"):
                    st.session_state.cleaned_data = None
                    st.rerun()
            
            # Detect issues
            cleaning_needs = self.data_cleaner.detect_issues(data_to_clean)
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Issues Found")
                if cleaning_needs['issues']:
                    for issue in cleaning_needs['issues']:
                        st.warning(f"• {issue['description']}")
                else:
                    st.success("No major issues detected!")
            
            with col2:
                st.subheader("Suggested Actions")
                if cleaning_needs['suggestions']:
                    for action in cleaning_needs['suggestions'][:5]:
                        st.info(f"• {action}")
            
            # Cleaning options
            if st.session_state.cleaned_data is None:
                st.subheader("Cleaning Configuration")
                
                cleaning_config = {}
                
                if cleaning_needs['missing_values']:
                    cleaning_config['handle_missing'] = st.selectbox(
                        "Handle Missing Values",
                        ["Keep as is", "Fill with mean", "Fill with median", "Fill with mode", "Drop rows"],
                        key="missing_handler"
                    )
                
                if cleaning_needs['duplicates'] > 0:
                    cleaning_config['remove_duplicates'] = st.checkbox(
                        f"Remove {cleaning_needs['duplicates']} duplicate rows",
                        value=True,
                        key="remove_dups"
                    )
                
                if cleaning_needs['outliers']:
                    cleaning_config['handle_outliers'] = st.checkbox(
                        "Handle outliers using IQR method",
                        value=False,
                        key="handle_outliers"
                    )
                
                cleaning_config['auto_convert_types'] = st.checkbox(
                    "Auto-convert data types",
                    value=True,
                    key="auto_convert"
                )
                
                if st.button("Apply Cleaning", type="primary"):
                    with st.spinner("Cleaning dataset..."):
                        cleaned_df, report = self.data_cleaner.clean(data_to_clean, cleaning_config)
                        st.session_state.cleaned_data = cleaned_df
                        st.session_state.cleaning_done = True
                        
                        st.success("Data cleaning completed!")
                        
                        st.subheader("Cleaning Report")
                        for action in report['actions_taken']:
                            st.write(f"✓ {action}")
                        
                        st.subheader("Cleaned Dataset Preview")
                        st.dataframe(cleaned_df.head(10), use_container_width=True)
            
            elif st.session_state.cleaned_data is not None:
                st.subheader("Cleaned Dataset")
                st.dataframe(st.session_state.cleaned_data.head(10), use_container_width=True)
        
        else:
            st.warning("Please complete Steps 1 and 2 first")
    
    def eda_step(self):
        """Step 4: Exploratory Data Analysis"""
        st.header("Exploratory Data Analysis")
        st.markdown("Discover patterns, trends, and relationships in your data.")
        
        data = st.session_state.cleaned_data if st.session_state.cleaned_data is not None else st.session_state.data
        
        if data is not None:
            if st.button("Run EDA", type="primary"):
                with st.spinner("Performing exploratory data analysis..."):
                    eda_results = self.eda_analyzer.analyze(data)
                    st.session_state.eda_results = eda_results
            
            if st.session_state.eda_results:
                eda_results = st.session_state.eda_results
                
                # Descriptive statistics
                st.subheader("Descriptive Statistics")
                st.dataframe(eda_results['descriptive_stats'], use_container_width=True)
                
                # Distribution analysis
                numeric_cols = data.select_dtypes(include=['number']).columns.tolist()
                if numeric_cols:
                    st.subheader("Distribution Analysis")
                    selected_col = st.selectbox("Select column", numeric_cols, key="dist_col")
                    
                    if selected_col in eda_results['distributions']:
                        dist = eda_results['distributions'][selected_col]
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Skewness", f"{dist['skewness']:.3f}")
                        with col2:
                            st.metric("Kurtosis", f"{dist['kurtosis']:.3f}")
                        with col3:
                            st.metric("Std Deviation", f"{dist['std']:.2f}")
                
                # Correlation analysis
                if len(numeric_cols) > 1:
                    st.subheader("Correlation Analysis")
                    st.dataframe(eda_results['correlations']['matrix'].style.background_gradient(cmap='coolwarm'), use_container_width=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Strong Positive Correlations**")
                        for corr in eda_results['correlations']['top_correlations'][:5]:
                            if corr['correlation'] > 0.5:
                                st.success(f"{corr['pair'][0]} ↔ {corr['pair'][1]}: {corr['correlation']:.3f}")
                    
                    with col2:
                        st.markdown("**Strong Negative Correlations**")
                        for corr in eda_results['correlations']['bottom_correlations'][:5]:
                            if corr['correlation'] < -0.5:
                                st.error(f"{corr['pair'][0]} ↔ {corr['pair'][1]}: {corr['correlation']:.3f}")
                
                # Key insights
                st.subheader("Key Insights")
                for insight in eda_results['key_insights'][:5]:
                    st.markdown(f'<div class="insight-card">{insight}</div>', unsafe_allow_html=True)
        
        else:
            st.warning("Please complete Steps 1-3 first")
    
    def dashboard_step(self):
        """Step 5: Interactive Dashboard"""
        st.header("Interactive Dashboard")
        st.markdown("Create custom visualizations to explore your data.")
        
        data = st.session_state.cleaned_data if st.session_state.cleaned_data is not None else st.session_state.data
        
        if data is not None:
            numeric_cols = data.select_dtypes(include=['number']).columns.tolist()
            
            col1, col2 = st.columns(2)
            
            with col1:
                x_var = st.selectbox("X-Axis Variable", data.columns.tolist(), key="x_var")
            
            with col2:
                if x_var in numeric_cols:
                    y_options = ["Count"] + numeric_cols
                else:
                    y_options = numeric_cols if numeric_cols else ["Count"]
                y_var = st.selectbox("Y-Axis Variable", y_options, key="y_var")
            
            # Chart type recommendation
            recommended = self.dashboard_generator.recommend_chart(x_var, y_var, data)
            st.info(f"Recommended chart type: {recommended}")
            
            chart_types = ['Bar Chart', 'Line Chart', 'Scatter Plot', 'Pie Chart', 'Histogram', 'Box Plot']
            chart_type = st.selectbox("Chart Type", chart_types, 
                                     index=chart_types.index(recommended) if recommended in chart_types else 0,
                                     key="chart_type")
            
            # On button click, generate chart and store in session state
            if st.button("Generate Visualization", type="primary"):
                with st.spinner("Creating visualization..."):
                    fig = self.dashboard_generator.create_chart(data, x_var, y_var, chart_type)
                    
                    if fig:
                        st.session_state.dashboard_fig = fig
                        
                        with st.spinner("Generating AI insights..."):
                            insight = self.insight_engine.analyze_visualization(
                                data, x_var, y_var, chart_type, fig
                            )
                            st.session_state.dashboard_insight = insight
                    else:
                        st.session_state.dashboard_fig = None
                        st.session_state.dashboard_insight = None
                        st.error("Failed to create visualization. Please check your column selections.")
                    st.rerun()
            
            # Display chart from session state (persists across reruns)
            if st.session_state.dashboard_fig is not None:
                st.plotly_chart(st.session_state.dashboard_fig, use_container_width=True)
                
                if st.session_state.dashboard_insight:
                    st.markdown("### AI-Generated Insight")
                    st.markdown(f'<div class="insight-card">{render_ai_content(st.session_state.dashboard_insight)}</div>', unsafe_allow_html=True)
                
                if st.button("Clear Visualization"):
                    st.session_state.dashboard_fig = None
                    st.session_state.dashboard_insight = None
                    st.rerun()
            
            # Quick statistics
            st.subheader("Quick Statistics")
            stat_cols = st.columns(3)
            
            if numeric_cols:
                with stat_cols[0]:
                    st.metric("Highest Value", f"{data[numeric_cols[0]].max():,.2f}")
                    st.caption(f"in {numeric_cols[0]}")
            
            if len(numeric_cols) > 1:
                with stat_cols[1]:
                    corr_val = data[numeric_cols[0]].corr(data[numeric_cols[1]]) if len(numeric_cols) > 1 else 0
                    st.metric("Correlation", f"{corr_val:.3f}")
                    st.caption(f"{numeric_cols[0]} vs {numeric_cols[1]}")
        
        else:
            st.warning("Please complete previous steps first")
    
    def ai_insights_step(self):
        """Step 6: AI-Powered Insights"""
        st.header("AI-Powered Insights")
        st.markdown("Get advanced analytics and business recommendations from AI.")
        
        data = st.session_state.cleaned_data if st.session_state.cleaned_data is not None else st.session_state.data
        
        if data is not None:
            if st.button("Generate Business Analysis", type="primary"):
                with st.spinner("AI is analyzing your data..."):
                    insights = self.insight_engine.generate_business_insights(data)
                    
                    # Only display sections that actually have distinct content
                    if insights.get('executive_summary'):
                        # Check if this section is different from the raw response (i.e., was parsed)
                        is_parsed = any(insights.get(k) != insights.get('executive_summary') for k in ['trends', 'anomalies', 'recommendations', 'risk_factors'] if insights.get(k))
                        
                        if is_parsed:
                            st.markdown("### Executive Summary")
                            st.markdown(f'<div class="insight-card">{render_ai_content(insights["executive_summary"])}</div>', unsafe_allow_html=True)
                    
                    if insights.get('trends') and insights.get('trends') != insights.get('executive_summary'):
                        st.markdown("### Identified Trends")
                        st.markdown(f'<div class="insight-card">{render_ai_content(insights["trends"])}</div>', unsafe_allow_html=True)
                    
                    if insights.get('anomalies') and insights.get('anomalies') != insights.get('executive_summary'):
                        st.markdown("### Anomalies and Outliers")
                        st.markdown(f'<div class="insight-card">{render_ai_content(insights["anomalies"])}</div>', unsafe_allow_html=True)
                    
                    if insights.get('recommendations') and insights.get('recommendations') != insights.get('executive_summary'):
                        st.markdown("### Business Recommendations")
                        st.markdown(f'<div class="insight-card">{render_ai_content(insights["recommendations"])}</div>', unsafe_allow_html=True)
                    
                    if insights.get('risk_factors') and insights.get('risk_factors') != insights.get('executive_summary'):
                        st.markdown("### Risk Factors")
                        st.markdown(f'<div class="insight-card">{render_ai_content(insights["risk_factors"])}</div>', unsafe_allow_html=True)
                    
                    # If no sections were successfully parsed, show the full response once
                    if not any(insights.get(k) and insights.get(k) != insights.get('executive_summary') for k in ['trends', 'anomalies', 'recommendations', 'risk_factors']):
                        st.markdown("### Analysis Results")
                        st.markdown(f'<div class="insight-card">{render_ai_content(insights.get("executive_summary", ""))}</div>', unsafe_allow_html=True)
            
            # Quick insights
            st.subheader("Quick Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Analyze Key Metrics"):
                    with st.spinner("Analyzing..."):
                        analysis = self.insight_engine.analyze_key_metrics(data)
                        st.markdown(f'<div class="insight-card">{render_ai_content(analysis)}</div>', unsafe_allow_html=True)
            
            with col2:
                if st.button("Assess Data Quality"):
                    with st.spinner("Assessing..."):
                        assessment = self.insight_engine.assess_data_quality(data)
                        st.markdown(f'<div class="insight-card">{render_ai_content(assessment)}</div>', unsafe_allow_html=True)
        
        else:
            st.warning("Please complete previous steps first")
    
    def conversational_step(self):
        """Step 7: Conversational Analytics"""
        st.header("Conversational Analytics")
        st.markdown("Ask questions about your data in natural language.")
        
        data = st.session_state.cleaned_data if st.session_state.cleaned_data is not None else st.session_state.data
        
        if data is not None:
            st.markdown("""
            <div class="card">
                <strong>AI Assistant</strong><br>
                Ask me anything about your data. I can help you understand trends, 
                find patterns, compare metrics, and provide business insights.
            </div>
            """, unsafe_allow_html=True)
            
            # Chat interface
            chat_container = st.container()
            
            with chat_container:
                for message in st.session_state.chat_history:
                    if message['role'] == 'user':
                        st.markdown(f"""
                        <div style="text-align: right; margin: 0.6rem 0;">
                            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 0.6rem 1.2rem; border-radius: 18px 18px 4px 18px; display: inline-block; max-width: 80%; box-shadow: 0 2px 8px rgba(102,126,234,0.2);">
                                {message['content']}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style="margin: 0.6rem 0;">
                            <div style="background-color: var(--bg-chat-bot); padding: 0.6rem 1.2rem; border-radius: 18px 18px 18px 4px; display: inline-block; max-width: 80%; border: 1px solid var(--chat-bot-border); color: var(--text-primary);">
                                <strong style="color: #667eea;">AI:</strong> {render_ai_content(message['content'])}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            
            # User input
            col1, col2 = st.columns([5, 1])
            with col1:
                user_question = st.text_input("Ask a question:", key="chat_input", placeholder="Type your question here...")
            
            with col2:
                if st.button("Send", type="primary"):
                    if user_question:
                        st.session_state.chat_history.append({'role': 'user', 'content': user_question})
                        
                        with st.spinner("Analyzing..."):
                            response = self.conversational_analytics.ask_question(data, user_question)
                        
                        st.session_state.chat_history.append({'role': 'assistant', 'content': response})
                        st.rerun()
            
            # Suggested questions
            st.markdown("### Suggested Questions")
            suggested_questions = [
                "What are the main trends in my data?",
                "Which variables are most correlated?",
                "Are there any outliers or anomalies?",
                "What business recommendations do you have?",
                "Summarize the key insights from this dataset"
            ]
            
            cols = st.columns(2)
            for i, q in enumerate(suggested_questions):
                with cols[i % 2]:
                    if st.button(q, key=f"suggest_{i}"):
                        st.session_state.chat_history.append({'role': 'user', 'content': q})
                        with st.spinner("Analyzing..."):
                            response = self.conversational_analytics.ask_question(data, q)
                        st.session_state.chat_history.append({'role': 'assistant', 'content': response})
                        st.rerun()
            
            # Clear chat button
            if st.button("Clear Chat History"):
                st.session_state.chat_history = []
                st.rerun()
        
        else:
            st.warning("Please complete previous steps first")
    
    def reporting_step(self):
        """Step 8: Reporting and Export"""
        st.header("Reporting and Export")
        st.markdown("Generate reports and export your results.")
        
        data = st.session_state.cleaned_data if st.session_state.cleaned_data is not None else st.session_state.data
        
        if data is not None:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Data Export")
                
                csv = data.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Cleaned Data (CSV)",
                    data=csv,
                    file_name="intelliai_cleaned_data.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
                if st.button("Generate Executive Summary", use_container_width=True):
                    with st.spinner("Generating executive summary..."):
                        summary = self.insight_engine.generate_executive_summary(data)
                        
                        st.markdown("### Executive Summary")
                        st.markdown(f'<div class="card">{render_ai_content(summary)}</div>', unsafe_allow_html=True)
                        
                        st.download_button(
                            label="Download Summary",
                            data=summary,
                            file_name="executive_summary.txt",
                            mime="text/plain"
                        )
            
            with col2:
                st.markdown("### Report Generation")
                
                if st.button("Generate Full Analytics Report", use_container_width=True):
                    with st.spinner("Generating comprehensive report..."):
                        report = self.insight_engine.generate_full_report(data)
                        
                        st.markdown("### Analytics Report Preview")
                        
                        with st.expander("Dataset Overview"):
                            st.write(f"Total Records: {len(data):,}")
                            st.write(f"Total Features: {len(data.columns)}")
                        
                        with st.expander("Statistical Summary"):
                            st.dataframe(data.describe(), use_container_width=True)
                        
                        with st.expander("AI Recommendations"):
                            if isinstance(report.get('recommendations'), list):
                                for rec in report['recommendations'][:5]:
                                    st.markdown(f"• {rec}")
            
            st.markdown("---")
            
            # Completion message
            st.success("""
            Analysis Complete!
            
            Your data has been successfully analyzed. The insights and reports are ready for decision-making.
            
            Next Steps:
            - Share reports with stakeholders
            - Upload new datasets for analysis
            - Use conversational AI for deeper insights
            """)
        
        else:
            st.warning("Please complete previous steps first")
    
    def run(self):
        """Main application runner"""
        self.render_header()
        self.render_sidebar()
        
        steps = {
            1: self.data_upload_step,
            2: self.data_profiling_step,
            3: self.data_cleaning_step,
            4: self.eda_step,
            5: self.dashboard_step,
            6: self.ai_insights_step,
            7: self.conversational_step,
            8: self.reporting_step
        }
        
        if st.session_state.current_step in steps:
            steps[st.session_state.current_step]()
        
        # Footer
        st.markdown("""
        <div class="footer">
            IntelliAI - AI-Powered Business Intelligence Platform | Developed by Nawal Shahid | © 2026 All rights reserved.
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    app = IntelliAI()
    app.run()