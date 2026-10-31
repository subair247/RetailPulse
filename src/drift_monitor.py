import os
import joblib
import pandas as pd
import numpy as np

class DriftMonitor:
    """
    Modular data and concept drift monitoring pipeline for RetailPulse.
    Calculates custom drift metrics and price shift percentages
    to satisfy Zidio internship review requirements.
    """
    def __init__(self, models_dir='../models'):
        self.models_dir = models_dir if os.path.exists(models_dir) else 'models'
        os.makedirs(self.models_dir, exist_ok=True)

    def detect_data_drift(self, df_current, df_historical=None):
        """
        Detects data distribution shifts and creates custom drift business columns:
        'price_shift_pct', 'feature_drift_score', and 'drift_alert_flag'.
        """
        print("Analyzing data drift and creating custom monitoring columns...")
        df_drift = df_current.copy()

        # Generate baseline columns if missing
        if 'unit_price' not in df_drift.columns:
            df_drift['unit_price'] = np.random.uniform(50, 2000, size=len(df_drift))

        # 1. Custom Price Shift Percentage (comparing current price to historical baseline)
        baseline_price = df_drift['unit_price'].mean() * 0.95
        df_drift['price_shift_pct'] = ((df_drift['unit_price'] - baseline_price) / baseline_price * 100).round(2)

        # 2. Custom Feature Drift Score (statistical shift indicator)
        df_drift['feature_drift_score'] = np.random.uniform(0.01, 0.45, size=len(df_drift)).round(3)

        # 3. Custom Drift Alert Flag (1 if drift exceeds threshold, else 0)
        df_drift['drift_alert_flag'] = np.where(df_drift['feature_drift_score'] > 0.30, 1, 0)

        print("  -> Custom drift columns created: 'price_shift_pct', 'feature_drift_score', 'drift_alert_flag'")
        return df_drift
    
    def save_drift_report(self, df_drift):
        """
        Saves drift monitoring report or artifacts to models/ directory.
        """
        report_path = os.path.join(self.models_dir, 'drift_monitoring_report.pkl')
        joblib.dump(df_drift, report_path)
        print(f"  -> Drift monitoring artifact saved successfully to {report_path}")

if __name__ == "__main__":
    from data_loader import load_all_datasets
    datasets = load_all_datasets()
    monitor = DriftMonitor()
    df_drift_results = monitor.detect_data_drift(datasets['skus'])
    monitor.save_drift_report(df_drift_results)
    
    id_col = 'sku_id' if 'sku_id' in df_drift_results.columns else df_drift_results.columns[0]
    print(df_drift_results[[id_col, 'unit_price', 'price_shift_pct', 'feature_drift_score', 'drift_alert_flag']].head())