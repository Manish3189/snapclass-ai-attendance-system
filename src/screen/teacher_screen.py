import streamlit as st
from src.ui.base_layout import style_background_dashboard, style_base_layer
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.database.db import check_teacher_exists ,create_teacher,teacher_login,get_teacher_subject
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_code
from src.components.subject_card import subject_card
from src.components.dialog_add_photo import add_photos_dialog
from src.pipelines.face_pipeline import predict_attendance
from src.components.dialog_attendace_result import attendance_result_dialog
import numpy as np
from datetime import datetime
import pandas as pd
from src.database.config import supabase 
from src.components.dialog_voice_attendance import voice_attendance_dialog
from src.database.db import get_attendance_for_teacher

def teacher_screen():

    style_background_dashboard()
    style_base_layer()
   
    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type =="login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()




def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    st.subheader(f"Welcome ,{teacher_data['name']}" , text_alignment='right')

    c1,c2 = st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Logout",type='secondary' ,key='Loginbackbtn', shortcut="control+backspace"):
            st.session_state['is_logged_in']=False
            del st.session_state.teacher_data
            st.rerun()

    st.space()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendance'

    tab1 ,tab2,tab3 = st.columns(3)
    with tab1:
        type1 = 'primary' if st.session_state.current_teacher_tab == 'take_attendance' else 'tertiary'
        if st.button('Take Attendance', type= type1 ,width='stretch',icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()
    with tab2:
        type2 = 'primary' if st.session_state.current_teacher_tab == 'manage_student' else 'tertiary'
        if st.button('Manage Subjects',type= type2 ,width='stretch',icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab = 'manage_student'
            st.rerun()

    with tab3:
        type3 ='primary' if st.session_state.current_teacher_tab == 'attendance_records' else 'tertiary'
        if st.button('Attendance Records',type= type3, width='stretch',icon=':material/cards_stack:'):
            st.session_state.current_teacher_tab = 'attendance_records'
            st.rerun()


    if st.session_state.current_teacher_tab == 'take_attendance':
        teacher_tab_take_attendance()
    if st.session_state.current_teacher_tab == 'manage_student':
            teacher_tab_manage_student()
    if st.session_state.current_teacher_tab == 'attendance_records':
            teacher_tab_attendance_records()




    footer_dashboard()               

def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data['teacher_id']
    st.header("Take Ai Attendance")

    if 'attendance_image' not in st.session_state:
        st.session_state.attendance_image =[]
        st.rerun()

    subjects = get_teacher_subject(teacher_id)

    if not subjects:
        st.warning("You havent created any  subject yet! Please Create on to begin!")
        return 

    subject_option  = {f"{s['name']} - {s['subject_code']}" : s['subject_id'] for s in subjects}

    col1,col2 =st.columns([3,1], vertical_alignment='bottom')
    with col1:
        selected_subject_label = st.selectbox('Select subject',options=list(subject_option.keys()))

    with col2:
        if st.button("📷 Add photos",type='primary',width='stretch'):
            add_photos_dialog()

    selected_subject_id = subject_option[selected_subject_label]

    st.divider()

    if st.session_state.attendance_image: 
        st.header("Added photos")
        galley_col = st.columns(4)

        for idx,img in enumerate(st.session_state.attendance_image):
            with galley_col[idx%4]:
                st.image(img,width='stretch',caption=f"photo {idx+1}")

    has_photos = bool(st.session_state.attendance_image)
    c1,c2,c3 = st.columns(3)
    with c1:
        if st.button('Clear all phots',type='tertiary',width='stretch',icon=':material/delete:',disabled= not has_photos):
            st.session_state.attendance_image = []
            st.rerun()

    with c2:
           
        if st.button('Run Face Analysis',width='stretch',icon=':material/analytics:',type='secondary',disabled=not has_photos):
            with st.spinner('Deep scanning classroom photos....'):
                all_detected_id = {}

                for idx,img in enumerate(st.session_state.attendance_image):
                    img_np = np.array(img.convert('RGB'))
                    detected,_,_ = predict_attendance(img_np)

                    if detected:
                        for sid in detected.keys():
                            student_id= int(sid)

                            all_detected_id.setdefault(student_id,[]).append(f'photos { idx+1}')

                enrolled_res = supabase.table('subject_student').select(" *,students(*)").eq('subject_id',selected_subject_id).execute()

                enrolled_students = enrolled_res.data

                if not enrolled_students:
                    st.warning("No students enrolled in this course")
                else:
                    
                    results, attendance_to_log  = [], []
                    current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

                    for node in enrolled_students:
                        student =  node['students']
                        sources = all_detected_id.get(int(student['student_id']),[])
                        is_present = len(sources) > 0

                        results.append({
                            "Name": student['name'],
                            "ID" : student['student_id'],
                            "Sources": ",".join(sources) if is_present else"-",
                            "Status": "✅Present" if is_present else "❌️Absent"
                        })

                        attendance_to_log.append({
                            'student_id': student['student_id'],
                            "subject_id": selected_subject_id,
                            "timestamp": current_timestamp,
                            "is_present": bool(is_present)
                        })
                    attendance_result_dialog(pd.DataFrame(results), attendance_to_log)
    with c3:
        if st.button("Use Voice Attedance",type='primary',width='stretch',icon=":material/mic:"):
             voice_attendance_dialog(selected_subject_id)





                   







def teacher_tab_manage_student():
    teacher_id = st.session_state.teacher_data['teacher_id']
    col1,col2= st.columns(2)
    with col1:
         st.header("Manage subjects",width='stretch')
    with col2:
        if st.button('Create New Subject',width='stretch'):
            create_subject_dialog(teacher_id)
   
    # List all the subjects
    subject =  get_teacher_subject(teacher_id)
    if subject:
        for sub in subject:

            stats =[
                ("👥 ","Students",sub['total_students']),
                ("🧑🏻‍💻","Classes",sub['total_classes'])
            ] 
        
        def share_btn():
            if st.button("Share Codes", key=f"share_{sub['subject_code']}", icon=":material/share:"):
                share_subject_code(sub['name'],sub['subject_code'])

        st.space()

        subject_card(
            name = sub['name'],
            code = sub['subject_code'],
            section = sub['section'],
            stats=stats,
            footer_callback = share_btn
        )

    else:
        st.info("NO SUBJECT FOUND. CREATE ONE ABOVE")





def  teacher_tab_attendance_records():
    st.header("Attendance_records")

    teacher_id = st.session_state.teacher_data['teacher_id']

    records = get_attendance_for_teacher(teacher_id)
    
    if not records :
        return
    data = []

    for r in records:
        ts = r.get('timestamp')

        data.append({ 
            "ts_group": ts.split(".")[0] if ts else None,
            "Time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "NA", 
            "Subject": r['subjects']['name'], 
            "Subject_Code": r['subjects']['subject_code'], 
            "is_present": bool(r.get('is_present', False))
        })
        

    df = pd.DataFrame(data)

    summary = (
        df.groupby(['ts_group','Time','Subject','Subject_Code'])
            .agg(
                Present_count = ('is_present','sum'),
                Total_count = ('is_present','count')
            ).reset_index()

        )

    summary['Attendance Stats'] = (
        "✅" + summary['Present_count'].astype(str) + "/"
        +summary['Total_count'].astype(str) + 'Student'
    )

    display_df = (summary.sort_values(by='ts_group',ascending=False)
                   [['Time','Subject','Subject_Code','Attendance Stats']]
             )
        
    st.dataframe(display_df, width='stretch', hide_index=True)




def login_teacher(username,password):
    if not username or not password:
        return False

    teacher = teacher_login(username,password)
    if teacher :
        st.session_state.user_role = 'teacher'
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True
    return False





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
         if st.button("Login",icon=':material/passkey:',shortcut='control+enter',width='stretch'):
             if login_teacher(teacher_username,teacher_password):
                 st.toast("welcome back! ", icon="🖐️")
                 import time
                 time.sleep(1)
                 st.rerun()
             else:
                 st.error("Invalid username and password comba")

    with btnc2:
         if st.button("Register Instead", type='primary' ,icon=':material/passkey:',width='stretch'):
            st.session_state.teacher_login_type = 'register'
            

    footer_dashboard()






def register_teacher(teacher_username, teacher_name, teacher_password, teacher_pass_confirm):
    if not teacher_username or not teacher_password or not teacher_name:
        return False, "All fields are required!"

    if check_teacher_exists(teacher_username):
        return False, "Username already taken"

    if teacher_password != teacher_pass_confirm:
        return False, "Password doesn't match"

    try:
        create_teacher(teacher_username, teacher_password, teacher_name)
        return True, "Successfully created! Login now"

    except Exception as e:
        print("ERROR:", e)
        return False, f"Unexpected error: {e}"





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
        if st.button("Register Now",icon=':material/passkey:',shortcut='control+enter',width='stretch'):
            success , message = register_teacher(teacher_username,teacher_name,teacher_password,teacher_pass_confirm)

            if success:
                st.success(message)
                import time 
                time.sleep(2)
                st.session_state.teacher_login_type = "login"
                st.rerun()

            else:
                st.error(message)
    with btnc2:
        if st.button("Login Instead", type='primary' ,icon=':material/passkey:',width='stretch'):
            st.session_state.teacher_login_type = "login"
    
    
    footer_dashboard()