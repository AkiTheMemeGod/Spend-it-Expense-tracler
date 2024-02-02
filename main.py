import streamlit
from assets import *
import Account, Expenses, Income, Report

st.set_page_config(page_title="Spend It", layout="wide", page_icon="💵")


class Multiapp:
    @staticmethod
    def run():
        center_title("", 100, "lime", "$pend It.", "center")
        option = option_menu(
            menu_title=None,
            options=["Account", "Expense", "Income", "Report"],
            orientation="horizontal",
            icons=["person-fill", "cash-coin", "cash", "file-earmark-bar-graph-fill"],
            default_index=0,
        )

        if option == "Account":
            Account.app()

        if option == "Expense":
            if st.session_state.username != "":
                Expenses.app()
            else:
                center_title("mid", 55, "red", "<br><br><br>⚠️ Login to save your inputs")

        if option == "Income":
            if st.session_state.username != "":
                Income.app()
            else:
                center_title("mid", 55, "red", "<br><br><br>⚠️ Login to save your inputs")
        if option == "Report":
            if st.session_state.username != "":
                Report.app()
            else:
                center_title("mid", 55, "red", "<br><br><br>⚠️ Login to view your report")

        # st.session_state
    run()
