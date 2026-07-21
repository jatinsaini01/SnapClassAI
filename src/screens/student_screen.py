import streamlit as st
from src.ui.style_base_layout import base_layout, portal_layout
from src.components.header import header_portal , student_teacher_header
from src.components.footer import footer
from PIL import Image
import numpy as np
import time
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_model
from src.database.db import get_all_students, create_student , get_student_subjects , get_student_attendence
from src.components.enroll_dialogue import enroll_dialog
from src.components.subject_card import subject_card
from src.database.db import unenroll_student_to_subject
def student_dashboard():
    student_teacher_header()
    student_data = st.session_state.student_data
    student_id = student_data['student_id']
    st.divider()
    st.markdown(f"<p style='font-size:2rem; text-align:center;'>Welcome, {student_data['name']}</p>",unsafe_allow_html=True)
    st.space()
    col1 , col2 = st.columns(2)
    with col1:
        st.markdown(f"<p style='font-size:2rem; text-align:center;'>Your Enrolled Subjects</p>",unsafe_allow_html=True)
    with col2:
        if st.button("Enroll in Subject" , width="stretch"):
            enroll_dialog()
    st.divider()
    with st.spinner("Loading your Enrolled Subjects"):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendence(student_id)
    stats_map = {}
    for log in logs:
        sid = log['subject_id']
        if sid not in stats_map:
            stats_map[sid] = {"total":0 , "attended":0}
        stats_map[sid]['total'] += 1
        if log.get('is_present'):
            stats_map[sid]['attended'] += 1
    cols = st.columns(2)
    for i,sub_node in enumerate(subjects):
        sub = sub_node['subjects']
        sid = sub['subject_id']
        stats = stats_map.get(sid,{"total":0 , "attended":0})
        def unenroll_btn():
            if st.button("Un-Enroll Subject" , width = "stretch"):
                unenroll_student_to_subject(student_id , sid)
        with cols[i%2]:
            subject_card(
                name = sub['name'],
                code = sub['subject_code'],
                section = sub['section'],
                stats = [
                    ("Total :",stats['total']),
                    ("Attended :",stats['attended'])
                ]
            )
            unenroll_btn()
def student_screen():
    base_layout()
    portal_layout()
    if 'student_data' in st.session_state:
        student_dashboard()
        return
    header_portal()
    if 'show_registration' not in st.session_state:
        st.session_state.show_registration = False

    st.markdown("<p style='font-size:2rem; text-align:center;'>Login using Face ID</p>", unsafe_allow_html=True)
    photo_source = st.camera_input("Position your face in center")

    if photo_source:
        img = Image.open(photo_source).convert("RGB")
        img = np.array(img, dtype=np.uint8)
        img = np.ascontiguousarray(img)
        st.write("dtype:", img.dtype, "shape:", img.shape, "contiguous:", img.flags['C_CONTIGUOUS'])
        with st.spinner("AI is scanning...."):
            detected, all_ids, num_faces = predict_attendance(img)
            if num_faces == 0:
                st.warning("face not found!")
            elif num_faces > 1:
                st.warning("Too many faces")
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    student = next((s for s in all_students if s['student_id'] == student_id), None)
                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = "student"
                        st.session_state.student_data = student
                        st.toast(f"Welcome back, {student['name']}")
                        time.sleep(1)
                        st.rerun()
                else:
                    st.info("Face not recognized! , you might be new student")
                    st.session_state.show_registration = True

    if st.session_state.show_registration:
        with st.container(border=True):
            st.markdown("<p style='font-size:2rem; text-align:center;'>Register new profile!</p>", unsafe_allow_html=True)
            new_name = st.text_input("Enter name", placeholder="jatin saini")
            if st.button("Create Account", icon=':material/arrow_outward:', icon_position='right'):
                if new_name:
                    if not photo_source:
                        st.warning("Please capture your face first!")
                    else:
                        with st.spinner("Creating Profile........"):
                            img = Image.open(photo_source).convert("RGB")
                            img = np.array(img, dtype=np.uint8)
                            img = np.ascontiguousarray(img)
                            st.write("dtype:", img.dtype, "shape:", img.shape, "contiguous:", img.flags['C_CONTIGUOUS'])
                            embeddings = get_face_embeddings(img)
                            if embeddings:
                                face_emb = embeddings[0].tolist()
                                voice_emb = None
                                response_data = create_student(new_name, face_embedding=face_emb, voice_embedding=voice_emb)
                                if response_data:
                                    train_model()
                                    st.session_state.is_logged_in = True
                                    st.session_state.user_role = "student"
                                    st.session_state.student_data = response_data[0]
                                    st.session_state.show_registration = False
                                    st.toast(f"Profile created! , Hi {new_name}")
                                    time.sleep(1)
                                    st.rerun()
                            else:
                                st.error("could not capture your face for registration")
                else:
                    st.warning("Please enter your name!")

    footer()
