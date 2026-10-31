import os
import pandas as pd 

def load_all_datasets(base_dir='../data/clean'):
    """
    Safely load all 6 RetailPulse datasets into a structured dictionary.
    Automatically handles relative path fallback.
    """
    if not os.path.exists(base_dir):
        base_dir = 'data/clean' if os.path.exists('data/clean') else '.'

    dataset_files = {
        'customers': 'customer_master.csv',
        'stores': 'store_master.csv',
        'skus': 'sku_master.csv',
        'inventory': 'inventory_snapshot.csv',
        'promotions': 'promotions.csv',
        'flags': 'sku_iventory_flags.csv'
    }
    loaded_data = {}
    print("--- Loading RetailPulse Datasets ---")
    for key, filename in dataset_files.items():
        filepath = os.path.join(base_dir, filename)
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            loaded_data[key] = df
            print(f"[SUCCESS] Loaded {key} ({filename}): {df.shape}")
    else:
        print(f"[WARNING] File not found: {filepath}")

    return loaded_data

if __name__ =="__main__":
    datasets = load_all_datasets()
    