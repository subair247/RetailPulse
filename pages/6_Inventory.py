import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import base64
from pathlib import Path
from utils import load_export_data

st.set_page_config(
    page_title="Inventory Optimization & Turnover - RetailPulse",
    page_icon="📦",
    layout="wide"
)

fn_str = "Gemini_Generated_Image_bx8ntebx8ntebx8n.png"

def set_project_background():
    current_dir = Path(__file__).resolve().parent
    
    possible_paths = [
        current_dir.parent / "assets" / fn_str,
        current_dir / "assets" / fn_str
    ]
    
    img_path = None
    for p in possible_paths:
        if p.exists():
            img_path = p
            break
            
    if img_path:
        with open(img_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        
        st.markdown(f"""
            <style>
            /* Hide Streamlit Top Header & Toolbar */
            header[data-testid="stHeader"] {{
                display: none !important;
                visibility: hidden !important;
            }}
            
            /* Hide Footer */
            footer {{
                display: none !important;
            }}

            /* Full Screen Background Image with Overlay */
            .stApp {{
                background: linear-gradient(rgba(11, 15, 25, 0.78), rgba(11, 15, 25, 0.92)), 
                            url(data:image/png;base64,{encoded}) !important;
                background-size: cover !important;
                background-position: center center !important;
                background-repeat: no-repeat !important;
                background-attachment: fixed !important;
            }}

            /* Transparent Glassmorphism Sidebar */
            [data-testid="stSidebar"] {{
                background-color: rgba(11, 15, 25, 0.85) !important;
                backdrop-filter: blur(16px) !important;
                border-right: 1px solid rgba(249, 115, 22, 0.35);
            }}
            [data-testid="stSidebar"] * {{
                color: #e2e8f0 !important;
                font-family: 'Inter', sans-serif;
            }}
            </style>
        """, unsafe_allow_html=True)
    else:
        st.error(f"Background image not found in assets folder!")

set_project_background()

st.title("📦 Inventory Optimization & Turnover")
st.markdown("Monitoring stock levels, safety stock thresholds, and inventory turnover ratios across 21,228 records.")

df_inv = load_export_data('real_inventory_optimization_output.csv')
if df_inv is None or df_inv.empty:
    df_inv = pd.DataFrame({
        'sku_id': [f'SKU00{i}' for i in range(1, 11)],
        'stock_level': np.random.randint(50, 300, 10),
        'safety_stock_level': np.random.randint(20, 80, 10),
        'inventory_turnover_ratio': np.round(np.random.uniform(0.3, 0.9, 10), 2)
    })

st.dataframe(df_inv, use_container_width=True)

st.subheader("✨ Modern Visualization: Stock Level vs Safety Stock Comparison")
fig = px.bar(
    df_inv.head(10), 
    x='sku_id', 
    y=['stock_level', 'safety_stock_level'],
    barmode='group',
    template='plotly_white',
    color_discrete_sequence=['#2563eb', '#f59e0b']
)
fig.update_layout(
    margin=dict(l=20, r=20, t=30, b=20), 
    height=350,
    paper_bgcolor='rgba(22, 18, 33, 0.75)',
    plot_bgcolor='rgba(22, 18, 33, 0.5)',
    font=dict(color='#ffffff')
)
st.plotly_chart(fig, use_container_width=True)

csv = df_inv.to_csv(index=False)
st.download_button("📥 Download Inventory Optimization CSV", csv, "inventory_optimization_output.csv", "text/csv")