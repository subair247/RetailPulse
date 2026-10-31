import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import base64
from pathlib import Path

st.set_page_config(
    page_title="Sales & Drift Monitoring Analytics - RetailPulse",
    page_icon="📈",
    layout="wide"
)

fn_str = "istockphoto-2286455984-1024x1024 (1).jpg"

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
                background: linear-gradient(rgba(11, 15, 25, 0.75), rgba(11, 15, 25, 0.90)), 
                            url(data:image/jpeg;base64,{encoded}) !important;
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

st.title("📈 Sales & Drift Monitoring Analytics")
st.markdown("SKU unit price shifts and data drift score monitoring.")

df_drift = pd.DataFrame({
    'sku_id': [f'SKU00{i}' for i in range(1, 15)],
    'unit_price': np.random.uniform(50, 500, 14),
    'price_shift_pct': np.random.uniform(-5.0, 8.5, 14),
    'drift_score': np.random.uniform(0.1, 0.9, 14)
})

st.dataframe(df_drift, use_container_width=True)

st.subheader("✨ Modern Visualization: Price Shift vs Drift Correlation")
fig = px.scatter(
    df_drift, 
    x='unit_price', 
    y='price_shift_pct',
    size='unit_price',
    color='drift_score',
    hover_name='sku_id',
    template='plotly_white',
    color_continuous_scale='Blues'
)
fig.update_layout(
    margin=dict(l=20, r=20, t=30, b=20), 
    height=350,
    paper_bgcolor='rgba(22, 18, 33, 0.75)',
    plot_bgcolor='rgba(22, 18, 33, 0.5)',
    font=dict(color='#ffffff')
)
st.plotly_chart(fig, use_container_width=True)

csv = df_drift.to_csv(index=False)
st.download_button("📥 Download Sales Drift CSV", csv, "sales_drift_output.csv", "text/csv")