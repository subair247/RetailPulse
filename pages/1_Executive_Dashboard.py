import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import base64
from pathlib import Path

st.set_page_config(
    page_title="Executive Performance Dashboard - RetailPulse",
    page_icon="📊",
    layout="wide"
)

def set_project_background():
    current_dir = Path(__file__).resolve().parent
    
    possible_paths = [
        current_dir.parent / "assets" / "istockphoto-1487588969-1024x1024 (1).jpg",
        current_dir / "assets" / "istockphoto-1487588969-1024x1024 (1).jpg"
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

            /* Full Screen Background Image using your assets folder image */
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

st.title("📊 Executive Performance Dashboard")
st.markdown("High-level overview of enterprise revenue, orders, and regional distribution.")

df_exec = pd.DataFrame({
    'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'],
    'Revenue ($M)': [1.2, 1.5, 1.8, 2.2, 2.5, 3.1, 3.4, 3.8, 4.2, 4.5],
    'Orders': [3200, 3500, 3900, 4200, 4600, 5100, 5400, 5800, 6200, 6500]
})

st.dataframe(df_exec, use_container_width=True)

st.subheader("✨ Modern Visualization: Monthly Revenue Growth Trend")

fig = px.line(
    df_exec, 
    x='Month', 
    y='Revenue ($M)', 
    markers=True,
    template='plotly_white',
    color_discrete_sequence=['#38bdf8']
)
fig.update_layout(
    margin=dict(l=20, r=20, t=30, b=20), 
    height=350,
    paper_bgcolor='rgba(22, 18, 33, 0.75)',
    plot_bgcolor='rgba(22, 18, 33, 0.5)',
    font=dict(color='#ffffff')
)
st.plotly_chart(fig, use_container_width=True)

csv = df_exec.to_csv(index=False)
st.download_button("📥 Download Executive Report CSV", csv, "executive_report.csv", "text/csv")