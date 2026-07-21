import streamlit as st
from src.database.congig import supabase
from src.database.db import enroll_student_to_subject
@st.dialog("Quick Enrollment")
def auto_enroll_subject(subject_code):
    student_id = st.session_state.student_data['student_id']
    res = supabase.table("subjects").select("subject_id , name").eq('subject_code',subject_code).execute()
    if not res.data:
        st.error("subject code not found!")
        if st.button("close"):
            st.query_params.clear()
            st.rerun()
        return
    subject = res.data[0]
    check = supabase.table("subjects_students").select("*").eq('subject_id',subject['subject_id']).eq('student_id',student_id).execute()
    if check.data:
        st.info("You are already enrolled")
        if st.button("close"):
            st.query_params.clear()
            st.rerun()
        return
    st.markdown(f"would you like to join {subject['name']}?")
    col1 , col2 = st.columns(2)
    with col1:
        if st.button("No thanks"):
            st.query_params.clear()
            st.rerun()
            return
    with col2:
        if st.button("Yes Enroll Now" , width="stretch"):
            enroll_student_to_subject(student_id , subject['subject_id'])
            st.success("Enrolled Sucessfully")
            st.query_params.clear()
            import time
            time.sleep(2)
            st.rerun()

