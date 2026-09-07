import streamlit as st
from src.database.db import create_subject
import segno
import io

@st.dialog("Share Class Link")
def share_subject_code(subject_name , subject_code):
    app_domain = "snapclass-main-ai-attendance.streamlit.app"
    join_url = f"{app_domain}/?join-code={subject_code}"

    st.header("Scan to join")
    qr = segno.make(join_url)    # generate the QR

    out = io.BytesIO() # temporary container in memory where your QR-code PNGimage is stored.

    qr.save(out,kind='png',scale=10, border=1)

    col1,col2 = st.columns(2)
    with col1:
        st.markdown('### copy link')
        st.code(join_url,language='text')
        st.code(subject_code,language='text')
        st.info('Copy this link to share on Whatsapp and Email')

    with col2:
        st.markdown("Scan to join")
        st.image(out.getvalue(),caption='QRCODE for class joining')



