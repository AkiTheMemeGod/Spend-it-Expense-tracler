import streamlit as st
from assets import Upload


def display():
    rep = Upload()
    PDFbyte = rep.generate_pdf(df_selection)
    base64_pdf = base64.b64encode(PDFbyte).decode('utf-8')

    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="1300" height="1000" type="application/pdf"></iframe>'
    pdf_display = F'<object data={base64_pdf} type="application/pdf" width="100%" height="100%"><p>Alternative text - include a link <a href="myfile.pdf">to the PDF!</a></p></object>'
    st.markdown(pdf_display, unsafe_allow_html=True)


clicked = st.button(label="Generate Report", on_click=lambda: display())

if clicked:
    st.sidebar.success("Downloaded Successfully")