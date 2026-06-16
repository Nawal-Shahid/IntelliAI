import os
from groq import Groq
from dotenv import load_dotenv
import pandas as pd
import json

# Load environment variables
load_dotenv()

class InsightEngine:
    """AI-powered insight generation using Groq's Llama model"""
    
    def __init__(self):
        self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        self.model = "llama-3.3-70b-versatile"  # Using Llama 3.3 70B
        
    def _get_prompt(self, context, question):
        """Construct prompt for the LLM"""
        return f"""You are IntelliAI, an expert business intelligence analyst. 
Analyze the following data context and provide insights.

Data Context:
{context}

Question/Task: {question}

Provide a clear, actionable, and professional response. Focus on business implications and recommendations.
If suggesting numbers, use the actual data provided. Be specific and avoid generic statements.
"""
    
    def analyze_visualization(self, data, x_var, y_var, chart_type, fig=None):
        """Generate insights for a specific visualization"""
        # Prepare data summary
        if y_var == 'Count':
            summary = f"Distribution of {x_var}:\n"
            summary += data[x_var].value_counts().head(10).to_string()
        else:
            summary = f"Relationship between {x_var} and {y_var}:\n"
            summary += f"Correlation: {data[x_var].corr(data[y_var]) if pd.api.types.is_numeric_dtype(data[x_var]) and pd.api.types.is_numeric_dtype(data[y_var]) else 'N/A'}\n"
            summary += f"Data sample:\n{data[[x_var, y_var]].head(10).to_string()}"
        
        context = f"""
Dataset Info: {len(data)} rows, {len(data.columns)} columns
Chart Type: {chart_type}
X-axis: {x_var}
Y-axis: {y_var}

Data Summary:
{summary}

Key Statistics:
- {x_var} unique values: {data[x_var].nunique()}
- {x_var} missing values: {data[x_var].isnull().sum()}
"""
        
        if y_var != 'Count' and y_var in data.columns:
            context += f"""
- {y_var} range: {data[y_var].min():.2f} to {data[y_var].max():.2f}
- {y_var} average: {data[y_var].mean():.2f}
"""
        
        question = f"Analyze this {chart_type.lower()} visualization showing {y_var} vs {x_var}. Identify trends, patterns, outliers, and provide business recommendations."
        
        return self._query_llm(context, question)
    
    def generate_business_insights(self, data):
        """Generate comprehensive business insights from dataset (single consolidated API call)"""
        context = self._prepare_data_context(data)
        
        question = """Analyze this dataset and provide a structured response covering ALL of the following sections (use the exact section headers below):

1. "executive_summary" - Provide an executive summary of this dataset. What are the most important things to know?

2. "trends" - Identify 3-5 key trends or patterns in this data.

3. "anomalies" - Are there any anomalies, outliers, or concerning patterns?

4. "recommendations" - What are 3-5 actionable business recommendations based on this data?

5. "risk_factors" - What potential risk factors should decision-makers be aware of?

Format your response with each section clearly labeled using the exact section headers in quotation marks."""
        
        response = self._query_llm(context, question)
        
        # Parse the structured response into sections
        insights = self._parse_sections(response)
        return insights
    
    def _parse_sections(self, response):
        """Parse LLM response into structured sections"""
        sections = {
            'executive_summary': response,
            'trends': response,
            'anomalies': response,
            'recommendations': response,
            'risk_factors': response
        }
        
        # Try to split by section headers
        section_keys = {
            'executive_summary': ['"executive_summary"', 'executive summary', '1.'],
            'trends': ['"trends"', 'key trends', '2.'],
            'anomalies': ['"anomalies"', 'anomalies', '3.'],
            'recommendations': ['"recommendations"', 'recommendations', '4.'],
            'risk_factors': ['"risk_factors"', 'risk factors', '5.']
        }
        
        # Simple splitting approach: find each section by its header
        for section_key, markers in section_keys.items():
            for marker in markers:
                idx = response.find(marker)
                if idx >= 0:
                    # Find where this section ends (next marker or end)
                    rest = response[idx:]
                    next_start = len(response)
                    for other_key, other_markers in section_keys.items():
                        if other_key == section_key:
                            continue
                        for other_marker in other_markers:
                            pos = rest.find(other_marker, 1)
                            if 0 < pos < next_start:
                                next_start = pos
                    sections[section_key] = rest[:next_start].strip()
                    break
        
        return sections
    
    def _prepare_data_context(self, data):
        """Prepare data context for LLM"""
        context = f"""
DATASET OVERVIEW:
- Total Records: {len(data):,}
- Total Columns: {len(data.columns)}
- Column Names: {', '.join(data.columns[:20])}{'...' if len(data.columns) > 20 else ''}

DATA TYPES:
"""
        for col in data.columns[:15]:
            context += f"- {col}: {data[col].dtype}\n"
        
        # Add statistical summary for numeric columns
        numeric_cols = data.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            context += "\nNUMERIC COLUMNS STATISTICS:\n"
            for col in numeric_cols[:10]:
                context += f"- {col}: Min={data[col].min():.2f}, Max={data[col].max():.2f}, Mean={data[col].mean():.2f}, Median={data[col].median():.2f}\n"
        
        # Add sample data
        context += f"\nSAMPLE DATA (first 5 rows):\n{data.head(5).to_string()}\n"
        
        # Add missing values info
        missing = data.isnull().sum()
        if missing.sum() > 0:
            context += f"\nMISSING VALUES:\n{missing[missing > 0].to_string()}\n"
        
        return context
    
    def _query_llm(self, context, question):
        """Query Groq LLM for insights"""
        try:
            prompt = self._get_prompt(context, question)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert business intelligence analyst. Provide concise, data-driven insights."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Insight generation temporarily unavailable. Error: {str(e)}"
    
    def analyze_key_metrics(self, data):
        """Quick analysis of key metrics"""
        context = self._prepare_data_context(data)
        question = "What are the 3-5 most important metrics in this dataset and why should business leaders care about them?"
        return self._query_llm(context, question)
    
    def assess_data_quality(self, data):
        """Assess data quality"""
        missing_pct = (data.isnull().sum().sum() / (len(data) * len(data.columns))) * 100
        duplicate_pct = (data.duplicated().sum() / len(data)) * 100
        
        context = f"""
Data Quality Metrics:
- Missing Values: {missing_pct:.1f}%
- Duplicate Rows: {duplicate_pct:.1f}%
- Total Rows: {len(data):,}
- Total Columns: {len(data.columns)}
"""
        
        question = "Assess the data quality based on the metrics provided. What are the main issues and how can they be addressed?"
        return self._query_llm(context, question)
    
    def generate_executive_summary(self, data):
        """Generate executive summary report"""
        context = self._prepare_data_context(data)
        question = """Generate a professional executive summary of this dataset including:
1. Overview of what the data represents
2. Key findings and insights
3. Critical metrics and their significance
4. Top 3 recommendations for action
5. Potential risks or limitations

Format as a business memo."""
        
        return self._query_llm(context, question)
    
    def generate_full_report(self, data):
        """Generate comprehensive analytics report"""
        context = self._prepare_data_context(data)
        question = """Generate a comprehensive analytics report with:
1. Executive Summary
2. Data Quality Assessment
3. Key Statistical Findings
4. Trend Analysis
5. Correlation Insights
6. Anomaly Detection Results
7. Actionable Recommendations
8. Next Steps

Make it detailed and business-focused."""
        
        response = self._query_llm(context, question)
        # Extract recommendations by looking for numbered items in the response
        lines = response.split('\n')
        recommendations = [line.strip() for line in lines if line.strip().startswith(('7.', '-', '•', 'Recommendation'))]
        if not recommendations:
            # Fallback: just take non-empty lines
            recommendations = [line.strip() for line in lines if line.strip()][:10]
        return {'report': response, 'recommendations': recommendations[:10]}