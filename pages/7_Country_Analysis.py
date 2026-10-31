import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import base64
from pathlib import Path

st.set_page_config(
    page_title="Regional Store & Country Analysis - RetailPulse",
    page_icon="🌍",
    layout="wide"
)

fn_str = "Gemini_Generated_Image_tbaw0stbaw0stbaw.png"

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

st.title("🌍 Regional Store & Country Analysis")
st.markdown("Sales contribution and store performance metrics across 30 operational stores and global markets.")

df_country = pd.DataFrame({
    'Country': ['India', 'USA', 'Germany', 'UK', 'UAE', 'Canada', 'Australia'],
    'Store_Count': [10, 8, 4, 3, 2, 2, 1],
    'Total_Sales ($)': [4500000, 6200000, 2800000, 1900000, 1200000, 950000, 800000]
})

st.dataframe(df_country, use_container_width=True)

st.subheader("✨ Modern Visualization: Regional Sales Contribution")
fig = px.pie(
    df_country, 
    names='Country', 
    values='Total_Sales ($)',
    hole=0.45,
    template='plotly_white',
    color_discrete_sequence=px.colors.qualitative.Prism
)
fig.update_traces(textinfo='percent+label')
fig.update_layout(
    margin=dict(l=20, r=20, t=30, b=20), 
    height=350,
    paper_bgcolor='rgba(22, 18, 33, 0.75)',
    plot_bgcolor='rgba(22, 18, 33, 0.5)',
    font=dict(color='#ffffff')
)
st.plotly_chart(fig, use_container_width=True)

csv = df_country.to_csv(index=False)
st.download_button("📥 Download Country Analysis CSV", csv, "country_analysis.csv", "text/csv")