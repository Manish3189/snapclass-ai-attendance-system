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
        color: #E0E3FF;
        text-align: center;
        font-size: 70px;
        font-weight: 900;
        line-height: 0.8;
        margin: 0;
        padding: 0;
    ">
        SNAP<br>CLASS
    </h1>
""", unsafe_allow_html=True)
def header_dashboard():

    base_dir = Path(__file__).resolve().parent
    logo_path = base_dir / "logo1.png"

    # Create 3 columns with the middle one centered
    c1, c2  = st.columns([0.9,2], vertical_alignment= 'center' , gap= 'small')

    with c1:
        # logo_col, text_col = st.columns([1, 2])
        # with logo_col:
        st.image(
            str(logo_path),
            width=100
        )

        # with text_col:
    with c2:
        st.markdown("""
                    <h2 style="
                    color:#5865f2;
                    font-size:70px;
                    font-weight:900;
                    line-height:0.8;
                    margin:0;
                    ">SNAP<br>CLASS
                    </h2>
        """, unsafe_allow_html=True)

    
          
    
        

    
    