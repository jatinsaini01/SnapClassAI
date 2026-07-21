import streamlit as st

def subject_card(name, code, section, stats=None, footer_callback=None):
    html = f"""
    <div style="background:white; border-radius:10px; padding:16px; margin-bottom:12px;">
        <h3>{name}</h3>
        <p>Code: {code} | Section: {section}</p>
    """

    if stats:
        html += "<div style='display:flex; gap:16px; margin-top:8px;'>"
        for label, value in stats:
            html += f"<div><b>{value}</b><br><small>{label}</small></div>"
        html += "</div>"

    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()