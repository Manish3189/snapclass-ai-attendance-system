import streamlit as st
from pathlib import Path


def header_home():

    base_dir = Path(__file__).resolve().parent
    logo_path = base_dir / "logo1.png"

    # Create 3 columns with the middle one centered
    c1, c2, c3 = st.columns([1.5, 1, 1])

    with c2:
        st.image(
            str(logo_path),
            width=100
        )

    st.markdown("""
        <h1 style="
            text-align:center;
            color:#E0E3FF;
            font-size:70px;
            font-weight:900;
            line-height:0.2;
        ">
            SNAP<br>CLASS</h1>
    """, unsafe_allow_html=True)