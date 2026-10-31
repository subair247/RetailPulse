import os
from data_loader import load_all_datasets
from clustering import CustomerSegmenter
from forecasting import DemandForecaster
from drift_monitor import DriftMonitor
from inventory_logic import InventoryManager

def run_retailpulse_pipeline():
    print("=" * 60)
    print("🚀 STARTING RETAILPULSE MLOPS END-TO-END PIPELINE")
    print("=" * 60)
    
    # Step 1: Load Datasets
    print("\n[Step 1/5] Loading all datasets...")
    datasets = load_all_datasets()
    
    # Step 2: Customer Segmentation & RFM Clustering
    print("\n[Step 2/5] Running Customer Segmentation & RFM Custom Features...")
    segmenter = CustomerSegmenter()
    df_rfm = segmenter.create_custom_rfm_features(datasets['customers'])
    segmenter.fit_kmeans_clusters(df_rfm)
    
    # Step 3: Demand Forecasting & Rolling Metrics
    print("\n[Step 3/5] Running Demand Forecasting & Inventory Trends...")
    forecaster = DemandForecaster()
    df_forecast = forecaster.create_custom_forecasting_features(datasets['inventory'])
    forecaster.save_forecasting_artifacts(df_forecast)
    
    # Step 4: Data Drift Monitoring & Price Shifts
    print("\n[Step 4/5] Running Data Drift & Price Shift Analysis...")
    monitor = DriftMonitor()
    df_drift = monitor.detect_data_drift(datasets['skus'])
    monitor.save_drift_report(df_drift)
    
    # Step 5: Inventory Optimization & Reorder Urgency
    print("\n[Step 5/5] Running Inventory Logic & Reorder Urgency Assessment...")
    manager = InventoryManager()
    df_inv = manager.create_custom_inventory_columns(datasets['inventory'])
    manager.save_inventory_artifacts(df_inv)
    
    print("\n" + "=" * 60)
    print("✅ SUCCESS: ALL PIPELINES EXECUTED & ARTIFACTS SAVED TO MODELS/")
    print("=" * 60)

if __name__ == "__main__":
    run_retailpulse_pipeline()