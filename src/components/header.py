import streamlit as st
def header_portal():
    _,col2, col3 ,_ = st.columns([1,4,2,1])
    with col2:
        st.markdown("""
            <h1 style='margin:0; text-align:center; white-space:nowrap; font-size:2.5rem;'>Snap Class</h1>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <style>
            div[data-testid="stButton"] > button {
                background-color: #EB459E !important;
                color: white !important;
                border-radius: 2rem !important;
                border: none !important;
                padding: 0.6rem 1.5rem !important;
                font-weight: 600 !important;
            }
            </style>
        """, unsafe_allow_html=True)
        if st.button("Go back to Home"):
            st.session_state['login_type'] = None
            st.session_state.pop('teacher_data', None)
            st.session_state.pop('is_logged_in', None)
            st.session_state.pop('user_role', None)
            st.session_state.pop('teacher_login_type', None)
            st.rerun()
def student_teacher_header():
    _,col2, col3 ,_ = st.columns([1,4,2,1])
    with col2:
        st.markdown("""
            <h1 style='margin:0; text-align:center; white-space:nowrap; font-size:2.5rem;'>Snap Class</h1>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <style>
            div[data-testid="stButton"] > button {
                background-color: #EB459E !important;
                color: white !important;
                border-radius: 2rem !important;
                border: none !important;
                padding: 0.6rem 1.5rem !important;
                font-weight: 600 !important;
            }
            </style>
        """, unsafe_allow_html=True)
        if st.button("Logout"):
           st.session_state['login_type'] = None
           st.session_state.pop('teacher_data', None)
           st.session_state.pop('student_data', None)   # <-- this line was missing
           st.session_state.pop('is_logged_in', None)
           st.session_state.pop('user_role', None)
           st.session_state.pop('teacher_login_type', None)
           st.rerun()
def header_home():
    logo_url = "https://img.icons8.com/?size=120&id=iUor4lyI46VF&format=png"
    st.markdown(f"""
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; margin-bottom:30px; margin-top:30px;">
            <img src='{logo_url}' style='height:100px;' />
            <h2 style='color:#E0E3F; text-align:center;'>Snap<br>Class</h2>
        </div>
    """, unsafe_allow_html=True)