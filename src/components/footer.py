import streamlit as st
from pathlib import Path


def footer_home():
     st.markdown("""
        <div style="
            margin-top: 2rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 5px;
        ">
            <p style="margin: 0; padding: 0;font-weight:bold ">Created By Manish Kumar Tailor</p>
            <p style="margin: 0; padding: 0;font-weight:bold ">🧑‍💻AI/ML Engineer</p>
        </div> 
    """, unsafe_allow_html=True)


def footer_dashboard():
     st.markdown("""
        <div style="
            margin-top: 2rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 5px;
            color:black;
        ">
            <p style="margin: 0; padding: 0;font-weight:bold ">Created By Manish Kumar Tailor</p>
            <p style="margin: 0; padding: 0;font-weight:bold ">🧑‍💻AI/ML Engineer</p>
        </div> 
    """, unsafe_allow_html=True)