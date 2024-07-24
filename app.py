import streamlit as st
import os

# User credentials
USER = 'admin'
PASSWORD = 'password'

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'selected_folder' not in st.session_state:
    st.session_state.selected_folder = None
if 'selected_page' not in st.session_state:
    st.session_state.selected_page = None

# Login function
def login(user, password):
    if user == USER and password == PASSWORD:
        st.session_state.logged_in = True
        st.rerun()
    else:
        st.error("Špatné heslo nebo příhlašovací jméno")

# Logout function
def logout():
    st.session_state.logged_in = False
    st.session_state.selected_folder = None
    st.session_state.selected_page = None
    st.rerun()


# Login Page
def login_page():
    st.title("Příhlášovací stránka")

    user = st.text_input("Přihlašovací jméno")
    password = st.text_input("Heslo", type="password")
    login_button = st.button("Login")

    if login_button:
        login(user, password)
        

# Load pages
def load_page(page_name, page_folder):
    page_path = os.path.join(page_folder, f"{page_name}.py")
    with open(page_path, encoding='utf-8') as f:
        code = compile(f.read(), page_path, 'exec')
        exec(code, globals())

# Main Page with Sidebar Navigation
def main_page():
    #st.sidebar.title("Navigace")
    st.write(f"Příhlášen uživatel: **{USER}**")

    
    GenPDF = st.Page(
        "reports/Generování pdf souboru.py", title="Generování pdf souboru",  default=True
    )
    ESLoad = st.Page("reports/Načtení dat z Elasticsearch.py", title="Načtení dat z Elasticsearch")

    TRange = st.Page("tools/Časové rozmezí.py", title="Časové rozmezí")
    report = st.Page("tools/Zpráva o průběhu provozu.py", title="Zpráva o průběhu provozu")
    CTree = st.Page("filter/condi_tr.py", title="Rozhodovací strom")



    if st.session_state.logged_in:
        pg = st.navigation(
            {
                "Statistiky A": [GenPDF, ESLoad],
                "Statistiky B": [TRange, report],
                "Filter": [CTree]
            }
        )
        pg.run()
    if st.sidebar.button("Logout", key="logout"):
        logout()
        st.rerun()



# Navigation
if st.session_state.logged_in:
    main_page()
else:
    login_page()
    
