import streamlit as st
from PIL import Image
@st.dialog("Caputre or Upload Photo")
def add_photos_dialogue():
    st.write("Add classroom photo for attendence")
    if 'photo_tab' not in st.session_state:
        st.session_state.photo_tab = 'camera'
    t1 , t2 = st.columns(2)
    with t1:
        if st.button("Camera",width="stretch"):
            st.session_state.photo_tab = 'camera'
    with t2:
        if st.button("Upload",width="stretch"):
            st.session_state.photo_tab = 'upload'
    if st.session_state.photo_tab == 'camera':
        cam_photo = st.camera_input("Take Photo",key="dialog_cam")
        if cam_photo:
            st.session_state.attendence_images.append(Image.open(cam_photo))
            st.toast("Photo Captured")
            st.rerun()
    if st.session_state.photo_tab == 'upload':
        uploaded_files = st.file_uploader("Upload Photos here",type = ['jpg','png','jpeg'],accept_multiple_files=True,key="dialog_upload")
        if uploaded_files:
            for f in uploaded_files:
                st.session_state.attendence_images.append(Image.open(f))
            st.toast("Photos Uploaded Successfully")
            st.rerun()
    st.divider()
    if st.button("Done",width="stretch"):
        st.rerun()          