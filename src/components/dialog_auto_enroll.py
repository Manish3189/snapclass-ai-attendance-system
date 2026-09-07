import streamlit as st
from src.database.db import create_subject
from src.database.config import supabase
import time
from src.database.db import enrolled_student_to_subject


@st.dialog("Quick Enrollment")
def auto_enroll_dialog(subject_code):
    student_id = st.session_state.student_data['student_id']

    res = supabase.table('subjects').select ('subject_id,name').eq('subject_code',subject_code).execute() 
    if not res.data:
        st.error("Subject code not found!")  
        if st.button("Close"):
            st.query_params.clear()
            st.rerun()
        return

    subject =res.data[0]

    check= supabase.table('subject_student').select('*').eq('subject_id',subject['subject_id']).eq('student_id',student_id).execute()

    if check.data:
        st.info("Your are already enrolled")
        if st.button('Got it!'):
            st.query_params.clear()
            st.rerun()
        return 
    ## if come is this line mean student not enroll this subject

    st.markdown(f"Would you like to enrolled in this **{subject['name']}**")

    col1,col2 = st.columns(2)
    with col1:
        if st.button('No thanks!'):
            st.query_params.clear()
            st.rerun() 
    with col2:
        if st.button("Yes enroll now!",type='primary',width='stretch'):
            enrolled_student_to_subject(student_id,subject['subject_id'])
            st.success("Joined successfully!.")
            st.query_params.clear()
            st.rerun()