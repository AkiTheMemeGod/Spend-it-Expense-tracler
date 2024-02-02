import streamlit as st
from streamlit_option_menu import option_menu


def center_title(pos, size, color, title, align="center"):
    if pos == "side":
        st.sidebar.markdown(f"""
                        <h1 style="font-family:monospace; color:{color}; font-size: {size}px;", align="{align}">{title}</h1>
""",
                            unsafe_allow_html=True)

    else:
        st.markdown(f"""
                <h1 style="font-family:monospace; color:{color}; font-size: {size}px;", align="{align}">{title}</h1>
""",
                    unsafe_allow_html=True)

