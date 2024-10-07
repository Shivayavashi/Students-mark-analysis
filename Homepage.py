import streamlit as st
import pymongo
from pymongo.server_api import ServerApi
from pymongo import MongoClient


import streamlit as st
st.title("Welcome to Homepage")
st.header("Student marks visualization")
st.write("Go to form section and fill the form and upload it to get your visualization")

# Connect to the DB.
# @st.experimental_singleton
@st.cache_data
def connect_db():
    client =  MongoClient('mongodb+srv://student:BkZU3akDij4V8tMs@cluster0.phhdmbo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
    db = client.get_database('Login')
    return db.User

user_db = connect_db()

# Initialize Session States.
if 'username' not in st.session_state:
       st.session_state.username = ''
if 'form' not in st.session_state:
       st.session_state.form = ''
        
# Key features selection, just to demonstrate how usernames are passed
def select_signup():
    st.session_state.form = 'signup_form'

def user_update(name):
    st.session_state.username = name

if st.session_state.username != '':
    st.write(f"You are logged in as {st.session_state.username.upper()}")

# Initialize Sing In or Sign Up forms
if st.session_state.form == 'signup_form' and st.session_state.username == '':
  
    signup_form = st.form(key='signup_form', clear_on_submit=True)
    new_username = signup_form.text_input(label='Enter Username*')
    new_user_email = signup_form.text_input(label='Enter Email Address*')
    new_user_pas = signup_form.text_input(label='Enter Password*', type='password')
    user_pas_conf = signup_form.text_input(label='Confirm Password*', type='password')
    note = signup_form.markdown('*required fields')
    signup = signup_form.form_submit_button(label='Sign Up')
    
    if signup:
        if '' in [new_username, new_user_email, new_user_pas]:
            st.error('Some fields are missing')
        else:
            if user_db.find_one({'log' : new_username}):
                st.error('Username already exists')
            if user_db.find_one({'email' : new_user_email}):
                st.error('Email is already registered')
            else:
                if new_user_pas != user_pas_conf:
                    st.error('Passwords do not match')
                else:
                    user_update(new_username)
                    user_db.insert_one({'log' : new_username, 'email' : new_user_email, 'pass' : new_user_pas})
                    st.success('You have successfully registered!')
                    st.success(f"You are logged in as {new_username.upper()}")
                    del new_user_pas, user_pas_conf
                    
elif st.session_state.username == '':
    login_form = st.form(key='signin_form', clear_on_submit=True)
    username = login_form.text_input(label='Enter Username')
    user_pas = login_form.text_input(label='Enter Password', type='password')
    
    if user_db.find_one({'log' : username, 'pass' : user_pas}):
        login = login_form.form_submit_button(label='Sign In', on_click=user_update(username))
        if login:
            st.success(f"You are logged in as {username.upper()}")
            del user_pas
    else:
        login = login_form.form_submit_button(label='Sign In')
        if login:
            st.error("Username or Password is incorrect. Please try again or create an account.")
else:
    logout = st.button(label='Log Out')
    if logout:
        user_update('')
        st.session_state.form = ''

# 'Create Account' button
if st.session_state.username == "" and st.session_state.form != 'signup_form':
    signup_request = st.button('Create Account', on_click=select_signup)
