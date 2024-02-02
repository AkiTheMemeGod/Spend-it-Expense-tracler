from assets import *

from dependencies.encrypter import encrypt


def app():

    with st.sidebar:
        center_title("side", 45, "#EBA0F6", "$pend It.", "center")
        c1, c2, c3 = st.columns([1.6, 4, 1])
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
        try:
            if st.session_state.username:
                with st.expander(label="EDIT 🖊️"):
                    center_title("s", 20, "#E23D9F", "🖼️CHANGE DISPLAY PICTURE", "center")

                    new_pfp = st.file_uploader("profile pic", type=['png', 'jpeg', ], label_visibility="hidden")

                    st.sidebar.markdown("###")
                    pfp = st.button('Change Profile Picture', use_container_width=True)
                    if pfp:
                        if new_pfp is not None:

                            new = Upload()
                            new.edit_pfp(st.session_state.username, new_pfp.read())
                            st.session_state.pfp = new_pfp
                            st.success("Your DP has been changed!")

                        else:
                            st.sidebar.error("Upload a file to change profile pic")
        except AttributeError:
            pass

        """center_title("s", 35, "#E23D9F", "🗑️DELETE ALL MY DATA", "center")

        delete = st.sidebar.button('Delete my data', use_container_width=True, type="primary")
        if delete:
            st.sidebar.button("Are you sure ?", use_container_width=True, type="primary")
        st.sidebar.markdown("---")"""
        st.sidebar.markdown("---")
        center_title("s", 35, "#E23D9F", "✒️ AUTHOR", "center")

        st.sidebar.link_button("Made by Akash",
                               url="https://akashportfolio.streamlit.app/",
                               use_container_width=True)

        st.sidebar.link_button("Contact Me",
                               url="https://akashportfolio.streamlit.app/Contact_Me",
                               use_container_width=True)

        st.sidebar.link_button("Application testing",
                               url="https://www.linkedin.com/in/rohith-fernando-86225b244/",
                               use_container_width=True)

    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''

    def f():
        try:
            auth = Fetch()

            usernames = auth.usernames()

            if username in usernames:
                # st.success("Correct usrs")

                password_to_check = auth.passwords(username)
                if password == password_to_check:
                    # st.success("Correct pass")
                    st.session_state.signedout = True
                    st.session_state.signout = True
                    st.session_state.username = username
                    st.session_state.pfp = auth.pfp(username)
                    st.session_state.useremail = auth.email(username)
                    st.session_state.pdf = ""

                else:
                    st.error("Wrong Password")

            else:
                st.error("Wrong Username")

        except Exception as e:
            st.error(e)

    def t():
        st.session_state.signout = False
        st.session_state.signedout = False
        st.session_state.username = ""
        st.session_state.pfp = ""
        st.session_state.useremail = ""
        st.session_state.pdf = ""


    if "signedout" not in st.session_state:
        st.session_state["signedout"] = False
    if 'signout' not in st.session_state:
        st.session_state['signout'] = False

    if not st.session_state["signedout"]:
        left_co, cent_co, last_co = st.columns([3, 7, 3])

        with cent_co:
            st.title("Your :red[Account] in :green[$pend It.]")
            acc = Upload()

            choice = st.radio('Login/Signup', ['Login', 'Sign up'],
                              horizontal=True,
                              label_visibility="hidden",
                              index=1,
                              key="radios")

            username = st.text_input('Username', key="log_usern")
            password = st.text_input('Password', type='password')

            if choice == 'Sign up':
                email = st.text_input("E-mail", key="new_usern")
                usr_pfp = st.file_uploader(label="Profile picture", type=['png', 'jpeg', ])

                if st.button('Create my account', use_container_width=True):
                    if usr_pfp is not None and username != "" and password != "":
                        acc.account(username, password, email, usr_pfp.read())
                        st.session_state["radios"].index = 0
                    elif username != "" and password != "":
                        acc.account(username, password, email, open("dependencies/pfp.png", "rb").read())
                    else:
                        st.error(":red[No empty fields please]")


            else:
                st.button('Login', on_click=f, use_container_width=True)

    if st.session_state.signout:
        st.markdown("""
        <style>
        .st-emotion-cache-1v0mbdj > img{
            border-radius: 50%;
            text-align: center;
            }
        </style>

        """, unsafe_allow_html=True)

        left_co, cent_co, last_co = st.columns([3, 7, 3])

        with cent_co:
            st.title("Your :red[Account] in :green[$pend It.]")
            st.markdown("###")
            # st.image(f"account/{str(st.session_state.username)}/pfp.png", width=200, caption=st.session_state.username)
            left_co, cent_co, last_co = st.columns(3)
            with cent_co:
                st.image(st.session_state.pfp, width=200)

            st.markdown("#")

            with st.container(border=0):
                st.info(f'Username :  {str(st.session_state.username)}')

                st.info(f'E-Mail :  {str(st.session_state.useremail)}')
                st.button('Sign out', on_click=t, use_container_width=True)
