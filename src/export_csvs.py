import pandas as pd
import os

os.makedirs('../data/exports', exist_ok=True)

# 1. Export Demand Forecast Results
if os.path.exists('../models/demand_forecast_features.pkl'):
    df_forecast = pd.read_pickle('../models/demand_forecast_features.pkl')
    df_forecast.to_csv('../data/exports/real_demand_forecast_output.csv', index=False)
    print("[SUCCESS] Exported real demand forecast CSV!")

# 2. Export Inventory Optimization Results
if os.path.exists('../models/inventory_optimization_report.pkl'):
    df_inv = pd.read_pickle('../models/inventory_optimization_report.pkl')
    df_inv.to_csv('../data/exports/real_inventory_optimization_output.csv', index=False)
    print("[SUCCESS] Exported real inventory optimization CSV!")

# 3. Export Drift Monitoring Results
if os.path.exists('../models/drift_monitoring_report.pkl'):
    df_drift = pd.read_pickle('../models/drift_monitoring_report.pkl')
    df_drift.to_csv('../data/exports/real_drift_monitoring_output.csv', index=False)
    print("[SUCCESS] Exported real drift monitoring CSV!")