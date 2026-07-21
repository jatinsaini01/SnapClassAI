import streamlit as st
from src.components.header import header_portal , student_teacher_header
from src.ui.style_base_layout import base_layout , portal_layout
from src.components.footer import footer
from src.database.db import teacher_exists , create_teacher , teacher_login , get_teacher_subjects , get_attendence_for_teacher
from src.components.dialogue_create_subject import create_subject_dialogue
from src.components.share_subject_dialogue import share_subject_dialogue
from src.components.subject_card import subject_card
from src.components.add_photos_dialogue import add_photos_dialogue
from src.pipelines.face_pipeline import predict_attendance
import numpy as np
from src.database.congig import supabase
from datetime import datetime, timezone, timedelta
import pandas as pd

IST = timezone(timedelta(hours=5, minutes=30))
from src.components.dialogue_attendence_result import attendence_result_dialogue
def teacher_screen():
    base_layout() 
    portal_layout()
    if "teacher_data" in st.session_state:
        teacher_dashboard()
        return
    elif 'teacher_login_type' not in st.session_state:
        st.session_state['teacher_login_type']='login'
    match st.session_state['teacher_login_type']:
        case 'login':
            teacher_screen_login() 
        case 'register':
            teacher_screen_register()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
#   Login Area
#------------------------------------------------------------------------------------------------------------------------------------------------------------------
def teacher_dashboard():
    student_teacher_header()
    teacher_data = st.session_state.teacher_data
    if 'current_teacher_tab' not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendence'
    st.divider()
    st.markdown(f"<p style='font-size:2rem; text-align:center;'>Welcome, {teacher_data['name']}</p>",unsafe_allow_html=True)
    st.space()
    #--------------------------------------------------------------------------------------------------------------------------
    tab1 , tab2 , tab3 = st.columns(3)
    with tab1:
        if st.button("Take Attendence" , width='stretch' , icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab = 'take_attendence'
            st.rerun()
    with tab2:
        if st.button("Manage Subjects" , width='stretch' , icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab = 'manage_subjects'
            st.rerun()
    with tab3:
        if st.button("Attendence Records" , width='stretch' , icon=':material/cards_stack:'):
            st.session_state.current_teacher_tab = 'attendence_records'
            st.rerun()
    st.divider()
    #----------------------------------------------------------------------------------------------------------------------------
    if st.session_state.current_teacher_tab == 'take_attendence':
        teacher_tab_take_attendence()
    if st.session_state.current_teacher_tab == 'manage_subjects':
        teacher_tab_manage_subjects()
    if st.session_state.current_teacher_tab == 'attendence_records':
        teacher_tab_attendence_records()
#-----------------------------------------------------------------------------------------------------------------------------------------------
def teacher_tab_take_attendence():
    teacher_id = st.session_state.teacher_data['teacher_id']
    st.markdown("<p style='font-size:2rem; text-align:center;'>Take Attendece</p>",unsafe_allow_html=True)
    if 'attendence_images' not in st.session_state:
        st.session_state.attendence_images = []
    subjects = get_teacher_subjects(teacher_id)
    if not subjects:
        st.warning("You have not created any subject yet")
        return
    subject_options = {f"{s['name']} - {s['subject_code']}" : s['subject_id'] for s in subjects}
    col1 , col2 = st.columns([3,1])
    with col1:
        selected_subject_label = st.selectbox("Select Subject",options=list(subject_options.keys()))
    with col2:
        if st.button("Add photos",icon=':material/photo_prints:',width="stretch"):
            add_photos_dialogue()
    selected_subject_id = subject_options[selected_subject_label]
    st.divider()
    if st.session_state.attendence_images:
        st.markdown("<p style='font-size:2rem; text-align:center;'>Added Photos</p>",unsafe_allow_html=True)
        galary_cols = st.columns(4)
        for idx,img in enumerate(st.session_state.attendence_images):
            with galary_cols[idx % 4]:
                st.image(img , width="stretch" , caption=f"photo {idx+1}")
        c1 , c2 = st.columns(2)
        with c1:
            if st.button("Clear Photos",width="stretch",icon=':material/delete:'):
                st.session_state.attendence_images = []
                st.rerun()
        with c2:
            has_photos = bool(st.session_state.attendence_images)
            if st.button("Run Face Analysis",width="stretch",icon=':material/analytics:'):
                with st.spinner("Deep Scanning Photos........."):
                    all_detected_ids = {}
                    for idx , img in enumerate(st.session_state.attendence_images):
                        img_np = np.array(img.convert('RGB'))
                        detected ,_ ,_ = predict_attendance(img_np)
                        if detected:
                            for sid in detected.keys():
                                student_id = int(sid)
                                all_detected_ids.setdefault(student_id , []).append(f"photo {idx+1}")
                    enroll_res = supabase.table("subjects_students").select("* , students(*)").eq('subject_id',selected_subject_id).execute()
                    enrolled_students = enroll_res.data
                    if not enrolled_students:
                        st.warning("No students in this course")
                    else:
                        results , attendence_to_log = [] , []
                        current_timestamp = datetime.now(timezone.utc).isoformat()
                        for node in enrolled_students:
                            student = node['students']
                            sources = all_detected_ids.get(int(student['student_id']),[])
                            is_present = len(sources)>0
                            results.append({
                                'name':student['name'],
                                'id':student['student_id'],
                                'source':", ".join(sources) if is_present else "-",
                                'status' : "Present" if is_present else "Absent"
                            })
                            attendence_to_log.append({
                                'student_id' : student['student_id'],
                                'subject_id' : selected_subject_id,
                                'timestamp' : current_timestamp,
                                'is_present' : bool(is_present)
                            })
                        attendence_result_dialogue(pd.DataFrame(results),attendence_to_log)

def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data['teacher_id']
    col1 , col2 = st.columns(2)
    with col1:
        st.markdown("<p style='font-size:2rem; text-align:center;'>Manage Subjects</p>",unsafe_allow_html=True)
    with col2:
        if st.button("Create New Subject",width="stretch"):
            create_subject_dialogue(teacher_id)
    # list all subjects
    subjects = get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                ("Students" , sub['total_students']),
                ("Classes" , sub['total_classes'])
            ]
        def share_btn():
            if st.button(f"Share code : {sub['name']}" , key = f"share_{sub['subject_id']}" , icon=':material/share:'):
                share_subject_dialogue(sub['name'],sub['subject_code'])
            st.space()
        subject_card(
            name = sub['name'],
            code = sub['subject_id'],
            section = sub['section'],
            stats = stats,
            footer_callback = share_btn
        )
    else:
        st.info("No Subject Found!")
def teacher_tab_attendence_records():
    st.markdown("<p style='font-size:2rem; text-align:center;'>Attendece records</p>",unsafe_allow_html=True)
    teacher_id = st.session_state.teacher_data['teacher_id']
    records = get_attendence_for_teacher(teacher_id)
    data = []
    if not records:
        return
    else:
        for r in records:
            ts = r.get("timestamp")
            if ts:
                dt = datetime.fromisoformat(ts)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                dt_ist = dt.astimezone(IST)
                time_str = dt_ist.strftime("%Y-%m-%d %I:%M %p")
                ts_group = dt_ist.strftime("%Y-%m-%d %H:%M:%S")
            else:
                time_str = "N/A"
                ts_group = None
            data.append({
                "ts_group":ts_group,
                "Time":time_str,
                "Subject":r['subjects']['name'],
                "Subject Code":r['subjects']['subject_code'],
                "is_present":bool(r.get('is_present',False))
            })
        df = pd.DataFrame(data)
        summary = (
            df.groupby(['ts_group','Time','Subject','Subject Code'])
            .agg(
                Present_Count = ('is_present','sum'),
                Total_Count = ('is_present','count'),
            ).reset_index()
        )
        summary['Attendence Stats'] = (
            summary['Present_Count'].astype(str) + " /" + summary['Total_Count'].astype(str) + 'Students'
        )
        display_df = (summary.sort_values(by='ts_group',ascending=False)
                     [['Time','Subject','Subject Code','Attendence Stats']]
        )
        st.dataframe(display_df,width="stretch",hide_index=True)
        

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
def login_teacher(teacher_username , teacher_password):
    if not teacher_username or not teacher_password:
        return False
    teacher = teacher_login(teacher_username , teacher_password)
    if teacher:
        st.session_state.user_role = 'teacher'
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True
    else:
        return False
def teacher_screen_login():
    header_portal()
    st.markdown("<p style='font-size:2rem; text-align:center;'>Login Your Teacher Profile</p>",unsafe_allow_html=True)
    teacher_username = st.text_input("Enter Username",placeholder="Jatin Saini")
    teacher_password = st.text_input("Enter Password" , type="password",placeholder="........")
    st.divider()
    col1 , col2 = st.columns(2)
    with col1:
        if st.button("Login" , icon=':material/passkey:' , width='stretch'):
            if login_teacher(teacher_username , teacher_password):
                st.toast("Login sucessfully!")
                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invaild username and password combo!")
    with col2:
        if st.button("Register" , icon=':material/passkey:' , width='stretch'):
            st.session_state['teacher_login_type']='register'
    footer()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#   REGISTER AREA
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
    # calls database functions
def register_teacher(teacher_name , teacher_username , teacher_password , confirm_teacher_password):
    if not teacher_name or not teacher_password or not teacher_username or not confirm_teacher_password:
        return False , "All feilds are necessary!"
    if teacher_exists(teacher_username):
        return False,"Username already taken!"
    if teacher_password != confirm_teacher_password:
        return False , "Password doesnt match"
    try:
        create_teacher(teacher_name , teacher_username , teacher_password)
        return True , "Teacher profile succesfully created , Login now!"
    except Exception as e:
        return False , "Unknown error occured!"
    # website teacher register area
def teacher_screen_register():
    header_portal()
    st.markdown("<p style='font-size:2rem; text-align:center;'>Register Your Teacher Profile</p>",unsafe_allow_html=True)
    teacher_name = st.text_input("Enter name" , placeholder="Jatin Kumar")
    teacher_username = st.text_input("Enter Username",placeholder="Jatin Saini")
    teacher_password = st.text_input("Enter Password" , type="password",placeholder="..........")
    confirm_teacher_password = st.text_input("Renter Password" , type="password",placeholder="..........")
    st.divider()
    col1 , col2 = st.columns(2)
    with col1:
        if st.button("Register" , icon=':material/passkey:' , width='stretch'):
            sucess , message = register_teacher(teacher_name , teacher_username , teacher_password , confirm_teacher_password)
            if sucess:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state['teacher_login_type'] = 'login'
                st.rerun()
            else:
                st.error(message)
    with col2:
        if st.button("Login" , icon=':material/passkey:' , width='stretch'):
            st.session_state['teacher_login_type']='login'
    footer()
