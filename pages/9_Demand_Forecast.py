import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import base64
from pathlib import Path
from utils import load_export_data

st.set_page_config(
    page_title="Demand Forecast & Rolling Trends - RetailPulse",
    page_icon="🎯",
    layout="wide"
)

fn_str = "Calculator and Demand Forecasting Infographic.png"  

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

            /* Full Screen Background Image with Professional Dark Overlay */
            .stApp {{
                background: linear-gradient(rgba(11, 15, 25, 0.82), rgba(11, 15, 25, 0.94)), 
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

st.title("🎯 Demand Forecast & Rolling Trends")
st.markdown("3-month rolling average demand predictions and stockout risk flags.")

df_forecast = load_export_data('real_demand_forecast_output.csv')
if df_forecast is None or df_forecast.empty:
    df_forecast = pd.DataFrame({
        'sku_id': [f'SKU00{i}' for i in range(1, 11)],
        'rolling_avg_demand': np.random.randint(50, 300, 10),
        'stockout_risk_flag': ['Low', 'Medium', 'Critical', 'Low', 'Low', 'Critical', 'Medium', 'Low', 'Critical', 'Low']
    })

st.dataframe(df_forecast, use_container_width=True)

st.subheader("✨ Modern Visualization: Rolling Demand Trend Analysis")

fig = px.area(
    df_forecast, 
    x='sku_id', 
    y='rolling_avg_demand',
    color='stockout_risk_flag',
    markers=True,
    template='plotly_white',
    color_discrete_map={'Low': '#10b981', 'Medium': '#f59e0b', 'Critical': '#ef4444'}
)
fig.update_layout(
    margin=dict(l=20, r=20, t=30, b=20), 
    height=350,
    paper_bgcolor='rgba(22, 18, 33, 0.75)',
    plot_bgcolor='rgba(22, 18, 33, 0.5)',
    font=dict(color='#ffffff')
)
st.plotly_chart(fig, use_container_width=True)

csv = df_forecast.to_csv(index=False)
st.download_button("📥 Download Demand Forecast CSV", csv, "demand_forecast_output.csv", "text/csv")