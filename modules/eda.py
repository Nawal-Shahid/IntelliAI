import pandas as pd
import numpy as np
from scipy import stats

class ExploratoryDataAnalyzer:
    """Performs comprehensive exploratory data analysis"""
    
    def analyze(self, df):
        """Complete EDA pipeline"""
        results = {
            'descriptive_stats': self._get_descriptive_stats(df),
            'distributions': self._analyze_distributions(df),
            'correlations': self._analyze_correlations(df),
            'anomalies': self._detect_anomalies(df),
            'key_insights': self._extract_insights(df)
        }
        
        return results
    
    def _get_descriptive_stats(self, df):
        """Generate descriptive statistics for all columns"""
        records = []
        
        for col in df.columns:
            col_stats = {
                'Column': col,
                'Type': str(df[col].dtype),
                'Unique': df[col].nunique(),
                'Missing': df[col].isnull().sum(),
                'Missing %': f"{(df[col].isnull().sum() / len(df)) * 100:.1f}%"
            }
            
            if pd.api.types.is_numeric_dtype(df[col]):
                col_stats.update({
                    'Min': df[col].min(),
                    'Max': df[col].max(),
                    'Mean': df[col].mean(),
                    'Median': df[col].median(),
                    'Std': df[col].std()
                })
            
            records.append(col_stats)
        
        return pd.DataFrame(records)
    
    def _analyze_distributions(self, df):
        """Analyze distribution characteristics of numeric columns"""
        distributions = {}
        
        numeric_cols = df.select_dtypes(include=['number']).columns
        
        for col in numeric_cols:
            clean_data = df[col].dropna()
            if len(clean_data) > 1:
                distributions[col] = {
                    'skewness': stats.skew(clean_data),
                    'kurtosis': stats.kurtosis(clean_data),
                    'mean': clean_data.mean(),
                    'median': clean_data.median(),
                    'std': clean_data.std(),
                    'q1': clean_data.quantile(0.25),
                    'q3': clean_data.quantile(0.75)
                }
        
        return distributions
    
    def _analyze_correlations(self, df):
        """Analyze correlations between numeric variables"""
        numeric_df = df.select_dtypes(include=['number'])
        
        if len(numeric_df.columns) < 2:
            return {
                'matrix': pd.DataFrame(),
                'top_correlations': [],
                'bottom_correlations': []
            }
        
        corr_matrix = numeric_df.corr()
        
        # Get top correlations
        corr_pairs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_pairs.append({
                    'pair': (corr_matrix.columns[i], corr_matrix.columns[j]),
                    'correlation': corr_matrix.iloc[i, j]
                })
        
        corr_pairs.sort(key=lambda x: x['correlation'], reverse=True)
        
        return {
            'matrix': corr_matrix,
            'top_correlations': corr_pairs[:10],
            'bottom_correlations': corr_pairs[-10:]
        }
    
    def _detect_anomalies(self, df):
        """Detect anomalies using IQR method"""
        anomalies = {}
        
        numeric_cols = df.select_dtypes(include=['number']).columns
        
        for col in numeric_cols:
            clean_data = df[col].dropna()
            if len(clean_data) > 0:
                Q1 = clean_data.quantile(0.25)
                Q3 = clean_data.quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 3 * IQR  # Stricter bound for anomalies
                upper_bound = Q3 + 3 * IQR
                
                outliers = clean_data[(clean_data < lower_bound) | (clean_data > upper_bound)]
                
                if len(outliers) > 0:
                    anomalies[col] = {
                        'count': len(outliers),
                        'values': outliers.tolist()[:10],
                        'percentage': (len(outliers) / len(clean_data)) * 100
                    }
        
        return anomalies
    
    def _extract_insights(self, df):
        """Extract key insights from the dataset"""
        insights = []
        
        # Basic dataset info
        insights.append(f"Dataset contains {len(df):,} rows and {len(df.columns)} columns")
        
        # Missing data insight
        missing_total = df.isnull().sum().sum()
        if missing_total > 0:
            missing_pct = (missing_total / (len(df) * len(df.columns))) * 100
            insights.append(f"Dataset has {missing_pct:.1f}% missing values overall")
        
        # Numeric insights
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            high_var_cols = []
            for col in numeric_cols:
                cv = df[col].std() / df[col].mean() if df[col].mean() != 0 else 0
                if cv > 1:
                    high_var_cols.append(col)
            
            if high_var_cols:
                insights.append(f"High variability detected in: {', '.join(high_var_cols[:3])}")
        
        # Categorical insights
        categorical_cols = df.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            for col in categorical_cols[:3]:
                top_value = df[col].mode()
                if len(top_value) > 0:
                    top_pct = (df[col].value_counts().iloc[0] / len(df)) * 100
                    insights.append(f"'{top_value.iloc[0]}' is the most common value in '{col}' ({top_pct:.1f}%)")
        
        # Correlation insight
        if len(numeric_cols) >= 2:
            corr_matrix = df[numeric_cols].corr()
            # Find highest correlation
            max_corr = 0
            max_pair = None
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_val = abs(corr_matrix.iloc[i, j])
                    if corr_val > max_corr and corr_val < 1:
                        max_corr = corr_val
                        max_pair = (corr_matrix.columns[i], corr_matrix.columns[j])
            
            if max_pair:
                insights.append(f"Strongest correlation ({max_corr:.2f}) between '{max_pair[0]}' and '{max_pair[1]}'")
        
        return insights