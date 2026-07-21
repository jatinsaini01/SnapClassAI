import streamlit as st
from src.ui.style_base_layout import base_layout , home_layout
from src.components.header import header_home
from src.components.footer import footer
def home_screen():
    base_layout()
    home_layout()
    header_home()
    _, col1, col2, _ = st.columns([1.75, 2, 2, 1])
    with col1:
        if st.button("Teacher Portal" , icon=':material/arrow_outward:' , icon_position='right'):
            st.session_state['login_type'] = 'teacher'
            st.rerun()
    with col2:
        if st.button("Student Portal" , icon=':material/arrow_outward:' , icon_position='right'):
            st.session_state['login_type'] = 'student'
            st.rerun()
    footer()