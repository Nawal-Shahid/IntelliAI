import pandas as pd
import numpy as np
from pathlib import Path
import io
import chardet
import re

class DataIngestion:
    """Handles data upload, validation, and initial loading"""
    
    def __init__(self):
        self.supported_formats = ['.csv', '.xlsx', '.xls']
        self.max_file_size_mb = 100
    
    def _detect_delimiter(self, raw_data):
        """Auto-detect CSV delimiter by examining the first line"""
        try:
            first_line = raw_data.decode('utf-8').split('\n')[0]
        except:
            try:
                first_line = raw_data.decode('latin1').split('\n')[0]
            except:
                return ','
        
        # Count occurrences of potential delimiters
        delimiters = [',', ';', '\t', '|']
        counts = {d: first_line.count(d) for d in delimiters}
        
        # Pick the delimiter with most occurrences (must have at least 2)
        best_delim = max(counts, key=counts.get)
        return best_delim if counts[best_delim] >= 2 else ','
    
    def ingest(self, uploaded_file):
        """
        Ingest and validate uploaded file
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            tuple: (dataframe, success, message)
        """
        try:
            # Validate file
            if uploaded_file is None:
                return None, False, "No file provided"
            
            # Check file size
            file_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
            if file_size_mb > self.max_file_size_mb:
                return None, False, f"File too large. Maximum size: {self.max_file_size_mb}MB"
            
            # Get file extension
            file_extension = Path(uploaded_file.name).suffix.lower()
            
            if file_extension not in self.supported_formats:
                return None, False, f"Unsupported file format. Supported: {', '.join(self.supported_formats)}"
            
            # Load based on file type
            if file_extension == '.csv':
                df = self._load_csv(uploaded_file)
            else:
                df = self._load_excel(uploaded_file)
            
            # Validate loaded data
            if df is None or df.empty:
                return None, False, "File is empty or could not be read"
            
            # Basic validation
            validation_result = self._validate_dataset(df)
            if not validation_result['is_valid']:
                return df, False, f"Dataset validation failed: {validation_result['message']}"
            
            # Convert column names to clean format
            df.columns = [str(col).strip().replace(' ', '_').lower() for col in df.columns]
            
            # Auto-detect and convert date columns
            df = self._auto_convert_dates(df)
            
            return df, True, f"Successfully loaded {len(df):,} rows with {len(df.columns)} columns"
            
        except Exception as e:
            return None, False, f"Error loading file: {str(e)}"
    
    def _load_csv(self, uploaded_file):
        """Load CSV file with encoding and delimiter detection"""
        try:
            raw_data = uploaded_file.getvalue()
            
            # Detect encoding
            encoding_result = chardet.detect(raw_data)
            encoding = encoding_result.get('encoding', 'utf-8')
            
            # Detect delimiter
            delimiter = self._detect_delimiter(raw_data)
            
            # Try different encodings
            encodings = [encoding, 'utf-8', 'latin1', 'iso-8859-1']
            
            for enc in encodings:
                try:
                    df = pd.read_csv(io.BytesIO(raw_data), encoding=enc, delimiter=delimiter)
                    if not df.empty and len(df.columns) > 1:
                        return df
                except:
                    continue
            
            # Fallback: try with delimiter detection and ignore errors
            for enc in encodings:
                try:
                    df = pd.read_csv(io.BytesIO(raw_data), encoding=enc, delimiter=delimiter, errors='ignore')
                    if not df.empty:
                        return df
                except:
                    continue
            
            # Last resort: try engine='python' with auto-detection
            return pd.read_csv(io.BytesIO(raw_data), engine='python', sep=None, encoding='utf-8', errors='ignore')
            
        except Exception as e:
            raise Exception(f"CSV loading failed: {str(e)}")
    
    def _load_excel(self, uploaded_file):
        """Load Excel file"""
        try:
            df = pd.read_excel(uploaded_file, sheet_name=0)
            return df
        except Exception as e:
            raise Exception(f"Excel loading failed: {str(e)}")
    
    def _validate_dataset(self, df):
        """Validate dataset structure and content"""
        validation = {
            'is_valid': True,
            'message': ''
        }
        
        if len(df.columns) < 1:
            validation['is_valid'] = False
            validation['message'] = "Dataset must have at least one column"
            return validation
        
        if len(df.columns) > 500:
            validation['is_valid'] = False
            validation['message'] = "Too many columns (max 500)"
            return validation
        
        if len(df) > 1000000:
            validation['message'] = "Large dataset detected. Performance may be impacted."
        
        empty_cols = df.columns[df.isnull().all()].tolist()
        if empty_cols:
            validation['message'] += f" Found {len(empty_cols)} completely empty columns."
        
        return validation
    
    def _auto_convert_dates(self, df):
        """Automatically detect and convert date columns"""
        for col in df.columns:
            if df[col].dtype == 'object':
                try:
                    # Try to convert to datetime
                    converted = pd.to_datetime(df[col], errors='coerce')
                    if converted.notna().sum() > len(df) * 0.8:  # If 80% successful
                        df[col] = converted
                except:
                    pass
        return df