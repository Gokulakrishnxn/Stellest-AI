#!/usr/bin/env python3
"""
Data Preprocessing for Stellest Lens Myopia Prediction
Handles data cleaning, feature engineering, and preparation for ML models
"""

import pandas as pd
import numpy as np
import os

class MyopiaDataPreprocessor:
    def __init__(self, data_file=None):
        self.data_file = data_file
        self.processed_data = None
        
    def preprocess_data(self):
        """Main preprocessing pipeline"""
        try:
            if self.data_file and os.path.exists(self.data_file):
                print(f"Loading data from {self.data_file}")
                data = pd.read_csv(self.data_file)
            else:
                print("Creating sample data for demonstration")
                data = self._create_sample_data()
            
            print(f"Original data shape: {data.shape}")
            
            # Clean data
            data = self._clean_data(data)
            
            # Engineer features
            data = self._engineer_features(data)
            
            # Handle missing values
            data = self._handle_missing_values(data)
            
            print(f"Processed data shape: {data.shape}")
            self.processed_data = data
            return data
            
        except Exception as e:
            print(f"Error in preprocessing: {e}")
            return self._create_sample_data()
    
    def _clean_data(self, data):
        """Clean the raw data"""
        # Remove duplicates
        data = data.drop_duplicates()
        
        # Convert data types
        numeric_columns = ['age', 'age_myopia_diagnosis', 'initial_power_re', 'initial_power_le',
                          'initial_axial_length_re', 'initial_axial_length_le', 'outdoor_time', 'screen_time']
        
        for col in numeric_columns:
            if col in data.columns:
                data[col] = pd.to_numeric(data[col], errors='coerce')
        
        return data
    
    def _engineer_features(self, data):
        """Create new features from existing data"""
        # Myopia duration
        if 'age' in data.columns and 'age_myopia_diagnosis' in data.columns:
            data['myopia_duration'] = data['age'] - data['age_myopia_diagnosis']
        
        # Average initial power
        if 'initial_power_re' in data.columns and 'initial_power_le' in data.columns:
            data['average_initial_power'] = (abs(data['initial_power_re']) + abs(data['initial_power_le'])) / 2
        
        # Average initial axial length
        if 'initial_axial_length_re' in data.columns and 'initial_axial_length_le' in data.columns:
            data['average_initial_al'] = (data['initial_axial_length_re'] + data['initial_axial_length_le']) / 2
        
        # Screen to outdoor ratio
        if 'screen_time' in data.columns and 'outdoor_time' in data.columns:
            data['screen_outdoor_ratio'] = data['screen_time'] / (data['outdoor_time'] + 0.1)
        
        # Create target variable (stellest_effectiveness)
        if 'stellest_effectiveness' not in data.columns:
            # Create synthetic target based on features
            data['stellest_effectiveness'] = self._create_synthetic_target(data)
        
        return data
    
    def _create_synthetic_target(self, data):
        """Create synthetic target variable for demonstration"""
        target = np.zeros(len(data))
        
        # Higher probability for younger patients
        if 'age' in data.columns:
            age_factor = np.where(data['age'] < 12, 0.8, np.where(data['age'] < 15, 0.6, 0.4))
            target += age_factor * 0.3
        
        # Higher probability for lower myopia
        if 'average_initial_power' in data.columns:
            myopia_factor = np.where(data['average_initial_power'] < 2, 0.8, 
                                   np.where(data['average_initial_power'] < 4, 0.6, 0.3))
            target += myopia_factor * 0.3
        
        # Higher probability for good outdoor time
        if 'outdoor_time' in data.columns:
            outdoor_factor = np.where(data['outdoor_time'] >= 2, 0.7, 
                                    np.where(data['outdoor_time'] >= 1, 0.5, 0.3))
            target += outdoor_factor * 0.2
        
        # Lower probability for high screen time
        if 'screen_time' in data.columns:
            screen_factor = np.where(data['screen_time'] > 6, 0.2, 
                                   np.where(data['screen_time'] > 3, 0.5, 0.8))
            target += screen_factor * 0.2
        
        # Add some randomness
        target += np.random.normal(0, 0.1, len(data))
        
        # Convert to binary
        target = (target > 0.5).astype(int)
        
        return target
    
    def _handle_missing_values(self, data):
        """Handle missing values in the dataset"""
        # Fill numeric columns with median
        numeric_columns = data.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            if data[col].isnull().any():
                data[col].fillna(data[col].median(), inplace=True)
        
        # Fill categorical columns with mode
        categorical_columns = data.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            if data[col].isnull().any():
                data[col].fillna(data[col].mode()[0], inplace=True)
        
        return data
    
    def _create_sample_data(self):
        """Create sample data for demonstration"""
        np.random.seed(42)
        n_samples = 250
        
        data = {
            'age': np.random.uniform(6, 18, n_samples),
            'age_myopia_diagnosis': np.random.uniform(4, 12, n_samples),
            'gender': np.random.choice([1, 2], n_samples),
            'family_history_myopia': np.random.choice([0, 1], n_samples),
            'outdoor_time': np.random.uniform(0.5, 4, n_samples),
            'screen_time': np.random.uniform(1, 8, n_samples),
            'previous_myopia_control': np.random.choice([0, 1], n_samples),
            'initial_power_re': -np.random.uniform(0.5, 6, n_samples),
            'initial_power_le': -np.random.uniform(0.5, 6, n_samples),
            'initial_axial_length_re': np.random.uniform(22, 26, n_samples),
            'initial_axial_length_le': np.random.uniform(22, 26, n_samples),
            'stellest_wearing_time': np.random.uniform(8, 16, n_samples)
        }
        
        return pd.DataFrame(data)
    
    def get_data_summary(self):
        """Get summary statistics of the processed data"""
        if self.processed_data is None:
            return "No data processed yet"
        
        summary = {
            'shape': self.processed_data.shape,
            'columns': list(self.processed_data.columns),
            'missing_values': self.processed_data.isnull().sum().to_dict(),
            'data_types': self.processed_data.dtypes.to_dict()
        }
        
        return summary
