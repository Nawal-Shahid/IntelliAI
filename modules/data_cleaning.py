import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer

class DataCleaner:
    """Intelligent data cleaning with recommendations"""
    
    def detect_issues(self, df):
        """Detect data quality issues and suggest cleaning actions"""
        issues = []
        suggestions = []
        
        # Check for missing values
        missing_cols = df.columns[df.isnull().any()].tolist()
        if missing_cols:
            issues.append({
                'type': 'missing_values',
                'description': f"Missing values found in {len(missing_cols)} columns",
                'columns': missing_cols
            })
            suggestions.append(f"Handle missing values in: {', '.join(missing_cols[:5])}")
        
        # Check for duplicates
        duplicate_count = df.duplicated().sum()
        if duplicate_count > 0:
            issues.append({
                'type': 'duplicates',
                'description': f"Found {duplicate_count} duplicate rows",
                'count': duplicate_count
            })
            suggestions.append(f"Remove {duplicate_count} duplicate rows")
        
        # Check for outliers in numeric columns
        outlier_cols = []
        numeric_cols = df.select_dtypes(include=['number']).columns
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))).sum()
            if outliers > 0:
                outlier_cols.append(col)
        
        if outlier_cols:
            issues.append({
                'type': 'outliers',
                'description': f"Outliers detected in {len(outlier_cols)} numeric columns",
                'columns': outlier_cols
            })
            suggestions.append(f"Handle outliers in: {', '.join(outlier_cols[:5])}")
        
        # Check for inconsistent data types
        for col in df.columns:
            if df[col].dtype == 'object':
                # Try to detect if column should be numeric
                numeric_test = pd.to_numeric(df[col], errors='coerce')
                if numeric_test.notna().sum() > len(df) * 0.8:
                    issues.append({
                        'type': 'data_type',
                        'description': f"Column '{col}' contains numbers stored as text",
                        'column': col
                    })
                    suggestions.append(f"Convert '{col}' from text to numeric type")
        
        return {
            'issues': issues,
            'suggestions': suggestions,
            'missing_values': len(missing_cols) > 0,
            'duplicates': duplicate_count,
            'outliers': len(outlier_cols) > 0
        }
    
    def clean(self, df, config):
        """
        Clean dataset based on configuration
        
        Args:
            df: Input dataframe
            config: Cleaning configuration dictionary
            
        Returns:
            tuple: (cleaned_df, cleaning_report)
        """
        cleaned_df = df.copy()
        report = {
            'actions_taken': [],
            'rows_affected': 0,
            'columns_modified': []
        }
        
        # Handle missing values
        if config.get('handle_missing') and config['handle_missing'] != 'Keep as is':
            original_rows = len(cleaned_df)
            
            if config['handle_missing'] == 'Drop rows':
                cleaned_df = cleaned_df.dropna()
                rows_dropped = original_rows - len(cleaned_df)
                report['actions_taken'].append(f"Dropped {rows_dropped} rows with missing values")
                report['rows_affected'] += rows_dropped
            
            elif config['handle_missing'] == 'Fill with mean':
                numeric_cols = cleaned_df.select_dtypes(include=['number']).columns
                for col in numeric_cols:
                    if cleaned_df[col].isnull().any():
                        cleaned_df[col] = cleaned_df[col].fillna(cleaned_df[col].mean())
                        report['actions_taken'].append(f"Filled missing values in '{col}' with mean")
                        report['columns_modified'].append(col)
            
            elif config['handle_missing'] == 'Fill with median':
                numeric_cols = cleaned_df.select_dtypes(include=['number']).columns
                for col in numeric_cols:
                    if cleaned_df[col].isnull().any():
                        cleaned_df[col] = cleaned_df[col].fillna(cleaned_df[col].median())
                        report['actions_taken'].append(f"Filled missing values in '{col}' with median")
                        report['columns_modified'].append(col)
            
            elif config['handle_missing'] == 'Fill with mode':
                for col in cleaned_df.columns:
                    if cleaned_df[col].isnull().any():
                        mode_value = cleaned_df[col].mode()
                        if len(mode_value) > 0:
                            cleaned_df[col] = cleaned_df[col].fillna(mode_value[0])
                            report['actions_taken'].append(f"Filled missing values in '{col}' with mode")
                            report['columns_modified'].append(col)
        
        # Remove duplicates
        if config.get('remove_duplicates', False):
            before_count = len(cleaned_df)
            cleaned_df = cleaned_df.drop_duplicates()
            after_count = len(cleaned_df)
            duplicates_removed = before_count - after_count
            if duplicates_removed > 0:
                report['actions_taken'].append(f"Removed {duplicates_removed} duplicate rows")
                report['rows_affected'] += duplicates_removed
        
        # Handle outliers
        if config.get('handle_outliers', False):
            numeric_cols = cleaned_df.select_dtypes(include=['number']).columns
            outliers_capped = 0
            
            for col in numeric_cols:
                Q1 = cleaned_df[col].quantile(0.25)
                Q3 = cleaned_df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers = ((cleaned_df[col] < lower_bound) | (cleaned_df[col] > upper_bound)).sum()
                if outliers > 0:
                    # Cap outliers
                    cleaned_df[col] = cleaned_df[col].clip(lower_bound, upper_bound)
                    outliers_capped += outliers
                    report['columns_modified'].append(col)
            
            if outliers_capped > 0:
                report['actions_taken'].append(f"Capped {outliers_capped} outlier values")
        
        # Convert data types
        if config.get('auto_convert_types', False):
            for col in cleaned_df.columns:
                if cleaned_df[col].dtype == 'object':
                    # Try numeric conversion
                    numeric_converted = pd.to_numeric(cleaned_df[col], errors='coerce')
                    if numeric_converted.notna().sum() > len(cleaned_df) * 0.8:
                        cleaned_df[col] = numeric_converted
                        report['actions_taken'].append(f"Converted '{col}' to numeric type")
                        report['columns_modified'].append(col)
        
        report['final_shape'] = cleaned_df.shape
        
        return cleaned_df, report