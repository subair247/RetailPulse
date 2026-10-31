import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import base64
from pathlib import Path

st.set_page_config(
    page_title="Customer Behavioral Analytics - RetailPulse",
    page_icon="👥",
    layout="wide"
)

fn_str = "istockphoto-2176461181-1024x1024 (1).jpg"

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

st.title("👥 Customer Behavioral Analytics")
st.markdown("Detailed customer purchasing patterns, lifetime value, and engagement frequency.")

df_cust = pd.DataFrame({
    'Customer_Segment': ['Frequent Buyers', 'Occasional Shoppers', 'High Spenders', 'Inactive'],
    'Average_Basket_Size': [450, 120, 890, 65],
    'Retention_Rate (%)': [85, 45, 92, 15]
})

st.dataframe(df_cust, use_container_width=True)

st.subheader("✨ Modern Visualization: Basket Size vs Customer Segments")
fig = px.bar(
    df_cust, 
    x='Customer_Segment', 
    y='Average_Basket_Size',
    color='Retention_Rate (%)',
    template='plotly_white',
    color_continuous_scale='Viridis'
)
fig.update_layout(
    margin=dict(l=20, r=20, t=30, b=20), 
    height=350,
    paper_bgcolor='rgba(22, 18, 33, 0.75)',
    plot_bgcolor='rgba(22, 18, 33, 0.5)',
    font=dict(color='#ffffff')
)
st.plotly_chart(fig, use_container_width=True)

csv = df_cust.to_csv(index=False)
st.download_button("📥 Download Customer Analytics CSV", csv, "customer_analytics.csv", "text/csv")