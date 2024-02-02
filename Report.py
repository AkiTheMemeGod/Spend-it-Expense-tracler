import base64
import struct
import pandas as pd
import plotly.express as px
from assets import *


def app():
    # try:
    c1, c2, c3 = st.columns([1, 8, 1])
    with c2:
        rep = Upload()
        df = pd.DataFrame(rep.all_data(), columns=["Date", "Month", "Category", "Type", "Amount", "Description"])
        # st.dataframe(df)
        with st.sidebar:

            center_title("s", 35, "#E23D9F", "🎯 FILTERS", "center")

            month = st.sidebar.multiselect(label="Select a Month",
                                           options=df["Month"].unique(),
                                           default=df["Month"].unique(),
                                           )

            category = st.sidebar.multiselect(label="Select a Category",
                                              options=df["Category"].unique(),
                                              default=df["Category"].unique(),
                                              )

            exp_type = st.sidebar.multiselect(label="Select a Type",
                                              options=df["Type"].unique(),
                                              default=df["Type"].unique(),
                                              )

            df_selection = df.query(
                "Month == @month & Category == @category & Type == @exp_type")

            # st.page_link(page="./main.py", label="Generate pdf")
            # st.page_link(page="pages/pdf.py", label="Generate pdf")
            def display(rep):
                # rep = Upload()
                PDFbyte = rep.generate_pdf(df_selection)
                base64_pdf = base64.b64encode(PDFbyte).decode('utf-8')

                pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="1300" height="1000" type="application/pdf"></iframe>'
                # pdf_display = F'<object data={base64_pdf} type="application/pdf" width="100%" height="100%"><p>Alternative text - include a link <a href="myfile.pdf">to the PDF!</a></p></object>'
                st.markdown(pdf_display, unsafe_allow_html=True)
                down = st.download_button(label=":red[Download Report]",
                                          data=PDFbyte,
                                          file_name="report.pdf",
                                          mime='application/octet-stream',
                                          use_container_width=True)
                if down:
                    st.sidebar.success("Downloaded Successfully")

            clicked = st.button(label="Generate Report", on_click= lambda: display(rep), use_container_width=True)

            if clicked:
                st.sidebar.success("Downloaded Successfully")

        center_title("s", 60, "#E23D9F", "📃Report", "center")
        co1, co2, co3 = st.columns([1, 8, 1])
        with co2:
            st.dataframe(df, use_container_width=False, hide_index=True, width=800)

        with st.container(border=False):
            center_title("s", 60, "#E23D9F", "📈Data", "center")

            l, c1, c2 = st.columns([1, 4.5, 4.5])

            try:
                with c1:

                    expense_df = df_selection[df_selection['Category'] == 'Expense']

                    grouped_df = expense_df.groupby('Type')['Amount'].sum().reset_index()

                    result_dict = dict(zip(grouped_df['Type'], grouped_df['Amount']))
                    fig1 = px.bar(grouped_df,
                                  x=grouped_df["Type"],
                                  y=grouped_df["Amount"],
                                  labels={"x": "Expenses", "y": "How much you spent"},
                                  width=250)
                    st.plotly_chart(fig1)

                with c2:
                    expense_df = df_selection[df_selection['Category'] == 'Income']

                    grouped_df = expense_df.groupby('Type')['Amount'].sum().reset_index()

                    result_dict = dict(zip(grouped_df['Type'], grouped_df['Amount']))
                    fig2 = px.bar(grouped_df,
                                  x=grouped_df["Type"],
                                  y=grouped_df["Amount"],
                                  labels={"x": "Income", "y": "How much you Earned"},
                                  width=250)
                    st.plotly_chart(fig2)

            except Exception:
                st.error("Enter at-least one entry in Income/Expenses")

        center_title("s", 60, "#E23D9F", "💰Total<br>", "center")

        with st.container(border=False):

            try:
                total_income = int(df_selection.groupby(by=['Category']).sum()[['Amount']]['Amount'][1])
                total_expense = int(df_selection.groupby(by=['Category']).sum()[['Amount']]['Amount'][0])
                savings = total_income - total_expense

                col4, col5, col6 = st.columns(3)
                with col4:
                    st.success(f"Total Income : {total_income}₹")
                with col5:
                    st.error(f"Total Expenses : {total_expense}₹")
                with col6:
                    if savings < 0:
                        st.error(f"Total Balance : {savings}₹")
                    if savings == 0:
                        st.warning(f"Total Balance : {savings}₹")
                    if savings > 0:
                        st.success(f"Total Balance : {savings}₹")
            except FutureWarning:
                pass
            except IndexError:
                st.error("Enter at-least one entry in Income/Expenses")

