from assets import *


def app():
    c1, c2, c3 = st.columns([3, 7, 3])
    with c2:
        exp = Upload()
        st.title("Expense Tracker")
        cat = "Expense"

        # expense = get_types("dependencies/expense_types.txt")

        types = st.selectbox(label="Select the type of expense:red[*]",
                             options=exp.types(cat.lower()),
                             key="exp_type")

        if types == "---Other---":
            other = st.text_input(label="Enter the type of expense: ")
            if other:
                exp.add_type(cat, other)

        amount = st.number_input(label="Amount:red[*]",
                                 placeholder="Enter the amount",
                                 key="exp_amt",
                                 min_value=0,
                                 max_value=10000000000,
                                 value=None,
                                 format="%d")

        desc = st.text_area(label="Description",
                            placeholder="Tell something about your expense..",
                            key="exp_desc")
        col1, col2 = st.columns(2)
        with col1:
            add_exp = st.button("Add Expense", use_container_width=True)

        with col2:
            st.button("Reset", on_click=reset_fields, use_container_width=True)

        if add_exp:
            exp.add_data(cat, types, str(amount), desc)
            st.success("Recorded Successfully")

