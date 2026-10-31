import os
import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler

class RetailPreprocessor:
    """
    Production preprocessor that converts string/categorical columns into
    machine-readable numerical format and scales numerical features.
    Saves encoders and scalers to the models/ directory.
    """
    def __init__(self, models_dir='../models'):
        self.models_dir = models_dir if os.path.exists(models_dir) else 'models'
        os.makedirs(self.models_dir, exist_ok=True)
        self.label_encoders = {}
        self.scaler = StandardScaler()
    
    def encode_categorical_columns(self, df, dataset_name, exclude_cols=None):
        """
        Automatically detects string (object) columns and converts them to integers.
        Skips primary ID columns or date columns specified in exclude_cols.
        """
        df_clean = df.copy()
        if exclude_cols is None:
            exclude_cols = []

        cat_cols = df_clean.select_dtypes(include=['object', 'category']).columns.tolist()
        cat_cols = [col for col in cat_cols if col not in exclude_cols]
        for col in cat_cols:
            le = LabelEncoder()
            df_clean[col] = le.fit_transform(df_clean[col].astype(str))
            self.label_encoders[f"{dataset_name}_{col}"] = le
            print(f"  -> Encoded string column '{col}' in [{dataset_name}] to numerical integers.")

        joblib.dump(self.label_encoders, os.path.join(self.models_dir, 'label_encoders.pkl'))
        return df_clean

        def scale_numerical_features(self, df, feature_cols, scaler_name='standard_scaler.pkl'):
            """
            Standardizes numerical features (mean=0, variance=1) for ML models like K-Means.
            """
        df_scaled = df.copy()
        df_scaled[feature_cols] = self.scaler.fit_transform(df_scaled[feature_cols])

        scaler_path = os.path.join(self.models_dir, scaler_name)
        joblib.dump(self.scaler, scaler_path)
        print(f"  -> Scaled features {feature_cols} and saved artifact to {scaler_path}")
        return df_scaled

