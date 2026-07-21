import streamlit as st
def base_layout():
    st.markdown("""
        <style>
           @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&family=Outfit:wght@100..900&display=swap');
           @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');
           #MainMenu , footer , header{
               visibility:hidden;
            }
            .block-container{
                padding-top:1.5rem !important;
            }
           h1{
               font-family:'Climate Crisis' , sans-serif !important;
               line-height:1.1 !important;
               margin-bottom:0rem !important;
           }
           h2{
               font-family:'Climate Crisis' , sans-serif !important;
               font-size:3.5rem !important;
               line-height:1.1 !important;
               margin-bottom:0rem !important;
           }
           h3 , h4 , p{
               font-family:'Outfit' , sans-serif !important;
           }
           button{
               background:#EB459E !important;
               border-radius:1.5rem !important;
               color:white !important;
               padding : 10px , 20px !important;
               border:None !important;
               transition:transform 0.25s ease-in-out !important;
           }
           button:hover{
               transform:scale(1.05) !important;
           }
        </style>
    
    """
    ,unsafe_allow_html=True)
def home_layout():
    st.markdown("""
        <style>
            .stApp{
                background:#5865F2 !important;
            }   
        </style>
    
    """
    ,unsafe_allow_html=True
)
def portal_layout():
    st.markdown("""
        <style>
            .stApp{
                background:#E0E3FF !important;
            }
        </style>
    """
    ,unsafe_allow_html=True)
