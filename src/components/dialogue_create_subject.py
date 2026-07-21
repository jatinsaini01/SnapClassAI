import streamlit as st
from src.database.db import create_subject
@st.dialog("Create New Subject")
def create_subject_dialogue(teacher_id):
    st.write("Enter details of new subject")
    subject_code = st.text_input("Enter subject code" , placeholder="B24-CSE-201")
    subject_name = st.text_input("Enter subject name" , placeholder="Introduction to Machine Learning")
    subject_section = st.text_input(" Enter section" , placeholder="A")
    subject_id = st.text_input("Enter subject id ",placeholder="1")
    if st.button("Create Subject" , width="stretch"):
        if subject_id and subject_name and subject_section and teacher_id and subject_id:
            try:
                create_subject(subject_code , subject_name , subject_section , teacher_id , subject_id)
                st.toast("Subject Cretaed Successfully")
                st.rerun()
            except Exception as e:
                st.error(f"Error : {str(e)}")
    else:
        st.warning("Please fill all the feilds")



