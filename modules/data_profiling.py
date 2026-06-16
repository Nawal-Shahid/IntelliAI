import pandas as pd
import numpy as np
from datetime import datetime

class DataProfiler:
    """Generates comprehensive data profiles and quality reports"""
    
    def generate_profile(self, df):
        """Generate complete dataset profile"""
        profile = {
            'total_records': len(df),
            'total_columns': len(df.columns),
            'column_types': {},
            'missing_values': {
                'total': 0,
                'by_column': {}
            },
            'duplicates': df.duplicated().sum(),
            'issues': [],
            'recommendations': []
        }
        
        # Analyze each column
        for col in df.columns:
            col_info = self._analyze_column(df[col])
            profile['column_types'][col] = col_info
            
            # Count missing values
            missing_count = df[col].isnull().sum()
            if missing_count > 0:
                profile['missing_values']['total'] += missing_count
                profile['missing_values']['by_column'][col] = missing_count
        
        # Identify issues
        profile['issues'] = self._identify_issues(df, profile)
        profile['recommendations'] = self._generate_recommendations(profile)
        
        return profile
    
    def _analyze_column(self, series):
        """Analyze individual column characteristics"""
        non_null = series.dropna()
        has_data = len(non_null) > 0
        
        analysis = {
            'detected_type': self._detect_type(series),
            'unique_count': series.nunique(),
            'sample_values': non_null.head(5).tolist() if has_data else [],
            'missing_count': series.isnull().sum(),
            'missing_percentage': (series.isnull().sum() / len(series)) * 100 if len(series) > 0 else 0
        }
        
        # Add numeric-specific analysis
        if pd.api.types.is_numeric_dtype(series) and has_data:
            analysis.update({
                'min': float(series.min()),
                'max': float(series.max()),
                'mean': float(series.mean()),
                'median': float(series.median()),
                'std': float(series.std())
            })
        
        return analysis
    
    def _detect_type(self, series):
        """Detect column data type"""
        if pd.api.types.is_datetime64_any_dtype(series):
            return 'datetime'
        elif pd.api.types.is_numeric_dtype(series):
            return 'numerical'
        elif pd.api.types.is_categorical_dtype(series):
            return 'categorical'
        else:
            # Try to detect if object column is actually categorical
            unique_ratio = series.nunique() / len(series)
            if unique_ratio < 0.05 and series.nunique() < 50:
                return 'categorical'
            return 'text'
    
    def _identify_issues(self, df, profile):
        """Identify data quality issues"""
        issues = []
        
        # Check for high missing values
        for col, missing_count in profile['missing_values']['by_column'].items():
            missing_pct = (missing_count / len(df)) * 100
            if missing_pct > 30:
                issues.append(f"Column '{col}' has {missing_pct:.1f}% missing values")
            elif missing_pct > 10:
                issues.append(f"Column '{col}' has {missing_pct:.1f}% missing values (moderate)")
        
        # Check for duplicates
        if profile['duplicates'] > 0:
            issues.append(f"Found {profile['duplicates']} duplicate rows")
        
        # Check for constant columns
        for col in df.columns:
            if df[col].nunique() == 1:
                issues.append(f"Column '{col}' has constant values (no variance)")
        
        # Check for high cardinality in categorical columns
        for col, info in profile['column_types'].items():
            if info['detected_type'] == 'categorical' and info['unique_count'] > 100:
                issues.append(f"Column '{col}' has high cardinality ({info['unique_count']} unique values)")
        
        # Check for outliers in numerical columns
        for col in df.select_dtypes(include=['number']).columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))).sum()
            if outliers > 0:
                outlier_pct = (outliers / len(df)) * 100
                if outlier_pct > 5:
                    issues.append(f"Column '{col}' has {outliers} potential outliers ({outlier_pct:.1f}% of data)")
        
        return issues
    
    def _generate_recommendations(self, profile):
        """Generate cleaning recommendations based on profile"""
        recommendations = []
        
        # Missing value recommendations
        if profile['missing_values']['total'] > 0:
            recommendations.append("Consider handling missing values through imputation or removal")
            
            # Specific recommendations for columns with high missing
            for col, missing_count in profile['missing_values']['by_column'].items():
                missing_pct = (missing_count / profile['total_records']) * 100
                if missing_pct > 50:
                    recommendations.append(f"Column '{col}' has >50% missing values - consider dropping it")
                elif missing_pct > 20:
                    recommendations.append(f"Column '{col}' has significant missing values - consider imputation")
        
        # Duplicate recommendations
        if profile['duplicates'] > 0:
            recommendations.append(f"Remove {profile['duplicates']} duplicate rows to clean the dataset")
        
        # Data type recommendations
        for col, info in profile['column_types'].items():
            if info['detected_type'] == 'text' and info['unique_count'] < 20:
                recommendations.append(f"Column '{col}' could be converted to categorical type for better performance")
        
        return recommendations
    
    def quality_score(self, df):
        """Calculate overall data quality score (0-100)"""
        score = 100
        
        # Penalize for missing values
        missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
        score -= missing_pct * 0.5
        
        # Penalize for duplicates
        duplicate_pct = (df.duplicated().sum() / len(df)) * 100
        score -= duplicate_pct * 2
        
        # Penalize for constant columns
        constant_cols = sum(1 for col in df.columns if df[col].nunique() == 1)
        score -= (constant_cols / len(df.columns)) * 10
        
        return max(0, min(100, score))