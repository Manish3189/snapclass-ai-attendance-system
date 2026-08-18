import streamlit as st
from pathlib import Path
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layer, style_background_home


def home_screen():
    base_dir = Path(__file__).resolve().parent
    logo_path1 = base_dir / "Teacher.png"
    logo_path2 = base_dir / "Student.png"
    header_home()
    style_background_home()
    style_base_layer()

    with st.container(key = "portal_box"):
        col1,col2 = st.columns(2)
        with col1 :
            st.header("I'm Student")
            st.image(str(logo_path2),width=100)

            if st.button('Student portal',type='primary',icon=':material/arrow_outward:',icon_position='right'):
                st.session_state['login_type'] = 'student' 
                st.rerun()

        with col2:
           st.header("I'm Teacher")
           st.image(str(logo_path1),width=95)
           if st.button('Teacher portal',type='primary' ,icon=':material/arrow_outward:',icon_position='right'):
               st.session_state['login_type'] = 'teacher' 
               st.rerun()

    footer_home()