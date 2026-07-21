import streamlit as st
from src.database.db import create_attendence
@st.dialog("Attendence Reports")
def attendence_result_dialogue(df , logs):
    st.write("please review  attendence before confirming")
    st.dataframe(df,width="stretch",hide_index=True)
    col1 , col2 = st.columns(2)
    with col1:
        if st.button("Discard",width="stretch"):
            st.rerun()
    with col2:
        if st.button("Confirm and Save" , width="stretch"):
            try:
                create_attendence(logs)
                st.toast("Attendence Taken")
                st.session_state.attendence_images = []
                st.rerun()
            except Exception as e:
                st.error("Sync Failed!")
