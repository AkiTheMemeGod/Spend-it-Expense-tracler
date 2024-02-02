import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3 as sq
import time as tt


def reset_fields():
    st.session_state["exp_desc"] = None
    st.session_state["exp_amt"] = None
    st.session_state["exp_type"] = None
    st.session_state["inc_desc"] = None
    st.session_state["inc_amt"] = None
    st.session_state["inc_type"] = None


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


class Fetch:
    def __init__(self):
        self.connection = sq.connect("spendit.db")

    def usernames(self):
        cursor = self.connection.cursor()
        cursor.execute("SElECT username FROM auth")
        users = cursor.fetchall()
        users = [i[0] for i in users]
        return users

    def passwords(self, usr):
        usr = (usr,)
        cursor = self.connection.cursor()
        cursor.execute(f"SElECT password FROM auth where username=?", usr)
        pwd = cursor.fetchone()[0]
        # pwds = [i[0] for i in pwds]
        return pwd

    def email(self, usr):
        usr = (usr, )
        cursor = self.connection.cursor()
        cursor.execute("SElECT email FROM auth where username=?", usr)
        emails = cursor.fetchone()[0]
        # emails = [i[0] for i in emails]
        return emails

    def pfp(self, usr):
        usr = (usr, )
        cursor = self.connection.cursor()
        cursor.execute("SElECT pfp FROM auth where username=?", usr)
        pfps = cursor.fetchone()[0]
        # pfps = [i[0] for i in pfps]
        return pfps

    def types(self, cat):
        cursor = self.connection.cursor()
        cursor.execute(f"SElECT {cat} FROM types")
        types = cursor.fetchall()
        types = [i[0] for i in types if i[0] is not None]
        return types


class Upload(Fetch):

    def add_data(self, cat, typ, amt, desc):
        amt = str(amt)
        data = (tt.strftime("%d-%m-%y"), tt.strftime("%B"), cat, typ, amt, desc)
        if amt.startswith("0"):
            amt = amt[1:]

        if not all([cat, typ, amt, desc]):
            st.warning("Please fill in all fields before adding an entry.")
            return

        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO report VALUES (?,?,?,?,?,?)", data)
        self.connection.commit()

    def edit_pfp(self, usr, pfp):
        data = (pfp, usr)
        cursor = self.connection.cursor()
        cursor.execute("Update auth set pfp=? where username=?", data)
        self.connection.commit()

    def account(self, usr, pwd, em, pfp):
        if usr in self.usernames():
            st.error("Username is Taken")

        else:
            data = (usr, pwd, em, pfp)
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO auth VALUES (?,?,?,?)", data)
            self.connection.commit()
            st.success("Successfully account created - Now Login")
            st.balloons()

    def add_type(self, cat, other):
        if other in self.types(cat.lower()):
            pass
        else:
            other = (other, )
            cursor = self.connection.cursor()
            cursor.execute(f"INSERT INTO types ({cat.lower()}) VALUES (?)", other)
            self.connection.commit()
