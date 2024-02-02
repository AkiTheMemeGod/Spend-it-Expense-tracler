import streamlit
from assets import *
import Account, Expenses, Income

st.set_page_config(page_title="Spend It", layout="wide", page_icon="💵")


class Multiapp:
    @staticmethod
    def run():

        center_title("side", 45, "#EBA0F6", "$pend It.", "center")
        c1, c2, c3 = st.sidebar.columns([1.6, 4, 1])
        with c2:
            try:
                if st.session_state.username:
                    st.markdown("""
                            <style>
                            .st-emotion-cache-1v0mbdj > img{
                                border-radius: 50%;
                                text-align: center;
                                }
                            </style>
                            """, unsafe_allow_html=True)
                    st.image(st.session_state.pfp,
                             width=150,
                             caption=f"Welcome back : {st.session_state.username}")
            except AttributeError:
                pass

        option = option_menu(
            menu_title=None,
            options=["Account", "Expense", "Income", "Report"],
            orientation="horizontal",
            icons=["person-fill", "cash-coin", "cash", "file-earmark-bar-graph-fill"],
            default_index=0,
        )
        center_title("", 100, "lime", "$pend It.", "center")
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


        # st.session_state
    run()
