import streamlit as st
def footer():
   st.markdown("""
        <style>
            .footer {
                position: fixed;
                left: 0;
                bottom: 0;
                width: 100%;
                background-color: black;
                color: white;
                text-align: center;
                padding: 10px 0;
            }
        </style>
        <div class="footer">
            <p>Created By Jatin Saini</p>
        </div>
    """, unsafe_allow_html=True)