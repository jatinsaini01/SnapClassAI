import streamlit as st
from src.database.congig import supabase
from src.database.db import enroll_student_to_subject , unenroll_student_to_subject
@st.dialog("Enroll in Subject")
def enroll_dialog():
    st.write("Enter the subject code provided by your teacher")
    join_code = st.text_input("Enter subject code",placeholder="B23-CSE-112")
    if st.button("Enroll Now" , width="stretch"):
        if join_code:
            res = supabase.table("subjects").select('name','subject_id','subject_code').eq("subject_code",join_code).execute()
            if res.data:
                subject = res.data[0]
                student_id = st.session_state.student_data['student_id']
                check = supabase.table("subjects_students").select("*").eq('subject_id',subject['subject_id']).eq('student_id',student_id).execute()
                if check.data:
                    st.warning("You are already enrolled in this subject")
                else:
                    enroll_student_to_subject(student_id , subject['subject_id'])
                    st.success("Sucessfully Enrolled!")
                    import time
                    time.sleep(1)
                    st.rerun()
        else:
            st.warning("Please enter subject code")

