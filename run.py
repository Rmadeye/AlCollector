import json

import streamlit as st
from streamlit import session_state
import mysql.connector

from src.db_handler import DBHandler  # assuming your DBHandler class is in a file named db_handler.py
from src.utils import calc_dil, plot_data
# Create an instance of DBHandler
if 'login' not in session_state: 
    session_state.login = False

db = DBHandler('stock', False)

st.set_page_config(page_title="AlCollector", page_icon=":cocktail:")

with open("db/login_access.json", "r") as login_file:
    login_cfg = json.load(login_file)

conn = mysql.connector.connect(**login_cfg)

st.title('Liquor database')

st.write('This is a simple app to manage your liquor database.')    

# make button for dynamic plotting

if 'show_plot' not in st.session_state:
    st.session_state.show_plot = False

if st.button('Plot'):
    st.session_state.show_plot = not st.session_state.show_plot
    
if st.session_state.show_plot:
    with st.form(key='select_features'):
        feature = st.selectbox('Select feature', ['volume', 'num_bottles'], key='plot_select')
        if st.form_submit_button('Plot'):
            fig = plot_data(db.get_all(), 'name', feature)
            st.pyplot(fig)

if 'show_all_data' not in st.session_state:
    st.session_state.show_all_data = True  # Initially, do not show all data

if st.button('Show all'):
    st.session_state.show_all_data = not st.session_state.show_all_data


if st.session_state.show_all_data:
    data = db.get_all()
    st.dataframe(data)


if st.button('Search'):
    st.session_state.show_search_form = not st.session_state.show_search_form

if 'show_search_form' not in st.session_state:
    st.session_state.show_search_form = False  # Initially hide the search form

if st.session_state.show_search_form:
    with st.form(key='search_form'):
        feature = st.selectbox('Select feature', ['id', 'name', 'voltage', 'volume', 'prod_date', 'num_bottles', 'description'], key='feature_select')
        value = st.text_input('Enter value', key='search_value_input')

        if st.form_submit_button('Find'):
            data = db.get_product(feature, value)
            if isinstance(data, str):
                st.write(data)
            else:
                st.dataframe(data)
if 'login' not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    with st.sidebar:
        username = st.text_input("Username")
        password = st.text_input("Password",type='password')

        if st.button('Login'):
            cursor = conn.cursor()
            query = "SELECT * FROM users WHERE username=%s AND password=%s"
            values = (username, password)
            cursor.execute(query, values)
            record = cursor.fetchone()
            if record:
                st.success("Logged in as {}".format(username))
                session_state.login = True
                session_state.username = username
            else:
                st.warning("Incorrect username or password")
            


if st.session_state.login:
    conn.close()
    with open("db/access.json", "r") as login_file:
        login_cfg = json.load(login_file)
    conn = mysql.connector.connect(**login_cfg)

    if st.button('Add'):
        st.session_state.show_add_form = not st.session_state.show_add_form

    if 'show_add_form' not in st.session_state:
        st.session_state.show_add_form = False  # Initially hide the add form

    if st.session_state.show_add_form:
        with st.form(key='add_form'):
            name = st.text_input('Enter name', key='name_input')
            voltage = st.number_input('Enter voltage', key='voltage_input', step=1)
            volume = st.number_input('Enter volume', key='volume_input', step=50)
            prod_date = st.date_input('Enter production date', key='prod_date_input')
            num_bottles = st.number_input('Enter number of bottles', key='num_bottles_input', step=1)
            description = st.text_input('Enter description', key='description_input')

            if st.form_submit_button('Add'):
                if not name or not voltage or not volume or not prod_date or not num_bottles or not description:
                    st.write("All fields must be filled.")
                else:
                    data = db.add_entry(name, voltage, volume, prod_date, num_bottles, description)
                    st.write(data)

    if st.button('Modify'):
        st.session_state.show_update_form = not st.session_state.show_update_form

    if 'show_update_form' not in st.session_state:
        st.session_state.show_update_form = False  # Initiall   y hide the update form

    if st.session_state.show_update_form:
        with st.form(key='update_form'):
            _id = st.number_input('Enter id', key='id_upd_input', step=1)
            feature = st.selectbox('Select feature', ['name', 'voltage', 'volume', 'prod_date', 'num_bottles', 'description'], key='update_select')
            value = st.text_input('Enter value', key='update_value_input')

            if st.form_submit_button('Update'):
                data = db.update_entry(_id, feature, value)
                st.write(data)  

    if st.button('Delete'):
        st.session_state.show_delete_form = not st.session_state.show_delete_form

    if 'show_delete_form' not in st.session_state:
        st.session_state.show_delete_form = False  # Initially hide the delete form

    if st.session_state.show_delete_form:
        with st.form(key='delete_form'):
            _id = st.number_input('Enter id', key='id_del_input', step=1)
            if st.form_submit_button('Delete'):
                data = db.delete_entry(_id)
                st.write(data)

else:
    st.write("Please log in to add, modify, or delete entries.")


if st.button('Calculate dilution'):
    st.session_state.show_calc_form = not st.session_state.show_calc_form

if 'show_calc_form' not in st.session_state:
    st.session_state.show_calc_form = False  # Initially hide the delete form

if st.session_state.show_calc_form:
    with st.form(key='calc_form'):
        volume = st.number_input('Enter volume', key='volume_input', step=50)
        initial_voltage = st.number_input('Enter current voltage', key='solution_input', step=1, min_value=1, max_value=99)
        final_voltage = st.number_input('Enter final voltage', key='final_input', step=1, min_value=1, max_value=99)
        if st.form_submit_button('Calculate'):
            data = calc_dil(volume, final_voltage, initial_voltage)
            st.write(f"You need to add {data[0]}ml of water to current {volume}ml of {initial_voltage}% voltage.")
            # total volume with %
            st.write(f"Result is {final_voltage}% {data[0]+volume} ml liquor.")    

