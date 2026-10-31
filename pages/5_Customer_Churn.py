import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import base64
from pathlib import Path

st.set_page_config(
    page_title="Customer Churn Risk Monitoring - RetailPulse",
    page_icon="⚠️",
    layout="wide"
)

fn_str = "Gemini_Generated_Image_rhju6jrhju6jrhju.png"

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

st.title("⚠️ Customer Churn Risk Monitoring")
st.markdown("Probability of customer churn across active engagement cohorts.")

df_churn = pd.DataFrame({
    'Cohort_Week': [f'Week {i}' for i in range(1, 9)],
    'Churn_Probability (%)': [12.5, 10.2, 14.8, 8.5, 7.2, 9.1, 6.4, 5.0]
})

st.dataframe(df_churn, use_container_width=True)

st.subheader("✨ Modern Visualization: Churn Risk Trend Over Time")
fig = px.area(
    df_churn, 
    x='Cohort_Week', 
    y='Churn_Probability (%)',
    markers=True,
    template='plotly_white',
    color_discrete_sequence=['#ef4444']
)
fig.update_layout(
    margin=dict(l=20, r=20, t=30, b=20), 
    height=350,
    paper_bgcolor='rgba(22, 18, 33, 0.75)',
    plot_bgcolor='rgba(22, 18, 33, 0.5)',
    font=dict(color='#ffffff')
)
st.plotly_chart(fig, use_container_width=True)

csv = df_churn.to_csv(index=False)
st.download_button("📥 Download Churn Report CSV", csv, "customer_churn_report.csv", "text/csv")