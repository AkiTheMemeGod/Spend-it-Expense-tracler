import random
from pathlib import Path
import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3 as sq
import time as tt
from fpdf import FPDF
import os
path = Path(__file__).parent / "pages/pdf.py"


def reset_fields():
    st.session_state["exp_desc"] = None
    st.session_state["exp_amt"] = None
    st.session_state["exp_type"] = None
    st.session_state["inc_desc"] = None
    st.session_state["inc_amt"] = None
    st.session_state["inc_type"] = None
    st.session_state["pdf"] = None


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

    def all_data(self, user):
        data = (user, )
        cursor = self.connection.cursor()
        cursor.execute("SElECT date, month, category, type, amount, description FROM report where user=?", data)
        users = cursor.fetchall()
        # users = [i[0] for i in users]
        return users

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

    def generate_pdf(self, df):

        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        pdf.set_font(family="Times", size=40, style="B")
        pdf.image(name="dependencies/logo.png", type="png", w=30, h=30, link="https://spend-it.streamlit.app")
        pdf.cell(w=20, h=10, txt='', align="C", ln=1)
        pdf.cell(w=20, h=10, txt='', align="C", ln=1)
        pdf.cell(w=20, h=10, txt='', align="C", ln=1)
        pdf.cell(w=20, h=10, txt='', align="C", ln=1)

        pdf.set_text_color(243, 18, 18)
        pdf.text(txt="$pend-It.", x=75, y=20)

        pdf.set_text_color(100, 100, 100)
        pdf.set_font(family="Times", size=20, style="B")
        pdf.text(txt="Expense Report", x=77, y=35)

        pdf.set_text_color(0, 0, 0)
        pdf.set_font(family="Times", size=18, style="B")
        pdf.text(txt=st.session_state.username, x=156, y=25)

        pdf.set_text_color(0, 0, 0)
        pdf.set_font(family="Times", size=18, style="B")
        pdf.text(txt=tt.strftime("Date : %d/%m/%y"), x=165, y=35)
        pdf.line(x1=10, x2=200, y1=45, y2=45)

        pdf.set_font(family="times", size=20, style="B")
        pdf.set_text_color(50, 50, 50)
        pdf.cell(w=20, h=10, txt='Date', align="C")

        pdf.cell(w=50, h=10, txt='Month', align="C")
        pdf.cell(w=40, h=10, txt='Category', align="C")
        pdf.cell(w=55, h=10, txt='Type', align="C")
        pdf.cell(w=32, h=10, txt='Amount', ln=1, align="C")
        pdf.cell(w=20, h=3, txt='', align="C")
        pdf.cell(w=50, h=3, txt='', align="C")
        pdf.cell(w=40, h=3, txt='', align="C")
        pdf.cell(w=55, h=3, txt='', align="C")
        pdf.cell(w=32, h=3, txt='', ln=1, align="C")

        for index, row in df.iterrows():
            try:
                pdf.set_font(family="Times", size=13)
                pdf.set_text_color(50, 50, 50)
                pdf.cell(w=20, h=10, txt=str(row['Date']), border=1, align="C")
                pdf.set_font(family="Times", size=16)
                pdf.set_text_color(50, 50, 50)
                pdf.cell(w=50, h=10, txt=str(row['Month']), border=1, align="C")
                pdf.cell(w=40, h=10, txt=str(row['Category']), border=1, align="C")
                pdf.cell(w=55, h=10, txt=str(row['Type']), border=1, align="C")
                pdf.cell(w=32, h=10, txt=str(row['Amount']), border=1, ln=1, align="C")
            except KeyError:
                pass
        try:
            total_income = str(df.groupby(by=['Category']).sum()[['Amount']]['Amount'][1])
            total_expense = str(df.groupby(by=['Category']).sum()[['Amount']]['Amount'][0])

            pdf.set_font(family="Times", size=25, style="B")
            pdf.cell(w=20, h=3, txt='', align="C")
            pdf.cell(w=50, h=3, txt='', align="C")
            pdf.cell(w=40, h=3, txt='', align="C")
            pdf.cell(w=55, h=3, txt='', align="C")
            pdf.cell(w=32, h=3, txt='', ln=1, align="C")
            pdf.set_text_color(33, 179, 42)
            pdf.cell(w=20, h=10, txt='', align="C")
            pdf.cell(w=50, h=10, txt='', align="C")
            pdf.cell(w=40, h=10, txt='Total', align="R")
            pdf.cell(w=55, h=10, txt='Income : ', align="L")
            pdf.cell(w=32, h=10, txt=total_income, ln=1, align="L")
            pdf.set_font(family="Times", size=25, style="B")

            pdf.cell(w=20, h=3, txt='', align="C")
            pdf.cell(w=50, h=3, txt='', align="C")
            pdf.cell(w=40, h=3, txt='', align="C")
            pdf.cell(w=55, h=3, txt='', align="C")
            pdf.cell(w=32, h=3, txt='', ln=1, align="C")
            pdf.set_text_color(255, 0, 0)
            pdf.cell(w=20, h=10, txt='', align="C")
            pdf.cell(w=50, h=10, txt='', align="C")
            pdf.cell(w=40, h=10, txt='Total', align="R")
            pdf.cell(w=55, h=10, txt='Expense : ', align="L")
            pdf.cell(w=32, h=10, txt=total_expense, ln=1, align="L")
        except Exception or FutureWarning or Warning:
            pass
        name = f"report{random.randint(100000000, 10000000000)}"
        pdf.output(name)

        PDFbyte = open(name, "rb").read()

        os.remove(name)
        return PDFbyte


class Upload(Fetch):

    def add_data(self, cat, typ, amt, desc):
        amt = str(amt)
        data = (tt.strftime("%d-%m-%y"), tt.strftime("%B"), cat, typ, amt, desc, st.session_state.username)
        if amt.startswith("0"):
            amt = amt[1:]

        if not all([cat, typ, amt, desc]):
            st.warning("Please fill in all fields before adding an entry.")
            return

        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO report VALUES (?,?,?,?,?,?,?)", data)
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
