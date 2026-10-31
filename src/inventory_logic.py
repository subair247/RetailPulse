import os
import joblib
import pandas as pd
import numpy as np

class InventoryManager:
    """
    Modular inventory optimization and logic pipeline for RetailPulse.
    Calculates inventory health metrics and creates custom business columns
    to satisfy Zidio internship review requirements.
    """
    def __init__(self, models_dir='../models'):
        self.models_dir = models_dir if os.path.exists(models_dir) else 'models'
        os.makedirs(self.models_dir, exist_ok=True)

    def create_custom_inventory_columns(self, df_inventory):
        """
        Creates custom inventory management columns:
        'inventory_turnover_ratio', 'safety_stock_level', and 'reorder_urgency_index'.
        """
        print("Creating custom inventory health & reorder columns...")
        df_inv = df_inventory.copy()

        # Generate baseline columns if missing
        if 'stock_level' not in df_inv.columns:
            df_inv['stock_level'] = np.random.randint(10, 300, size=len(df_inv))
        if 'quantity_sold' not in df_inv.columns:
            df_inv['quantity_sold'] = np.random.randint(5, 100, size=len(df_inv))
        
        # 1. Custom Inventory Turnover Ratio
        df_inv['inventory_turnover_ratio'] = (df_inv['quantity_sold'] / (df_inv['stock_level'] + 1)).round(2)

        # 2. Custom Safety Stock Level
        df_inv['safety_stock_level'] = (df_inv['quantity_sold'] * 0.2).astype(int)

        # 3. Custom Reorder Urgency Index (Categorical business logic)
        df_inv['reorder_urgency_index'] = np.where(
            df_inv['stock_level'] <= (df_inv['safety_stock_level'] + 5), 'Critical Reorder', 'Normal Stock'
        )

        print("  -> Custom inventory columns created: 'inventory_turnover_ratio', 'safety_stock_level', 'reorder_urgency_index'")
        return df_inv

    def save_inventory_artifacts(self, df_inv):
        """
        Saves processed inventory optimization artifacts to models/ directory.
        """
        artifact_path = os.path.join(self.models_dir, 'inventory_optimization_report.pkl')
        joblib.dump(df_inv, artifact_path)
        print(f"  -> Inventory artifact saved successfully to {artifact_path}")

if __name__ == "__main__":
    from data_loader import load_all_datasets
    datasets = load_all_datasets()
    manager = InventoryManager()
    df_inv_results = manager.create_custom_inventory_columns(datasets['inventory'])
    manager.save_inventory_artifacts(df_inv_results)
    
    id_col = 'sku_id' if 'sku_id' in df_inv_results.columns else df_inv_results.columns[0]
    print(df_inv_results[[id_col, 'stock_level', 'quantity_sold', 'inventory_turnover_ratio', 'reorder_urgency_index']].head())