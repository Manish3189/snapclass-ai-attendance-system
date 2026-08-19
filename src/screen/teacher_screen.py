import streamlit as st
from src.ui.base_layout import style_background_dashboard, style_base_layer
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard

def teacher_screen():

    style_background_dashboard()
    style_base_layer()
   

    if 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type =="login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()


def teacher_screen_login():
    c1,c2 = st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home",type='secondary' ,key='Loginbackbtn', shortcut="Ctrl+backspace"):
            st.session_state['login_type']=None
            st.rerun()
                        
    st.markdown("""<h2 style=" color: black; text-align: center;
                ">Login using Password
                </h2>
            """, unsafe_allow_html=True)
    st.space()
    st.space()

    teacher_username= st.text_input("Enter Username",placeholder='BOB')

    teacher_password= st.text_input("Enter Passwoed", type='password',placeholder='Enter password')
    st.divider()


    btnc1,btnc2=st.columns(2)
    with btnc1:
         st.button("Login",icon=':material/passkey:',shortcut='control+enter',width='stretch')
    with btnc2:
         if st.button("Register Instead", type='primary' ,icon=':material/passkey:',width='stretch'):
            st.session_state.teacher_login_type = 'register'
            

    footer_dashboard()

def teacher_screen_register():
    c1,c2 = st.columns(2,vertical_alignment='center',gap='xxlarge')  
    with c1:
            header_dashboard()
    with c2:
        if st.button("Go back to Home",type='secondary' ,key='Loginbackbtn', shortcut="Ctrl+backspace"):
            st.session_state['login_type'] = None
            st.rerun()
                 
    st.markdown("""
                    <h2 style="
                    color: black;
                    ">Register Your Teacher Profile
                    </h2>
                """, unsafe_allow_html=True)

    st.space()
    st.space()

    teacher_username= st.text_input("Enter Username",placeholder='BOB')

    teacher_name= st.text_input("Enter Name",placeholder='BOB Sharma')
    
    teacher_password= st.text_input("Enter Password", type='password',placeholder='Enter password')

    teacher_pass_confirm = st.text_input("Confirm Password", type='password' , placeholder='confirm password')

    st.divider()
    
    
    btnc1,btnc2=st.columns(2)
    with btnc1:
        st.button("Register Now",icon=':material/passkey:',shortcut='control+enter',width='stretch')
    with btnc2:
        if st.button("Login Instead", type='primary' ,icon=':material/passkey:',width='stretch'):
            st.session_state.teacher_login_type = "login"
    
    
    footer_dashboard()