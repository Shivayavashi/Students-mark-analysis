import streamlit as st
from pymongo import MongoClient

st.title("Welcome to Homepage")
st.header("Student marks visualization")
st.write("Go to form section and fill the form and upload it to get your visualization")
st.header('Hello 🌎!')

import streamlit as st

# Create an empty container
placeholder = st.empty()

actual_email = "email"
actual_password = "password"

# Insert a form in the container
with placeholder.form("login"):
    st.markdown("#### Enter your credentials")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Sign_in")
    
client = MongoClient('mongodb+srv://student:visualization@cluster0.phhdmbo.mongodb.net/?retryWrites=true&w=majority')
db = client['Login']
doc_body={
    "email":email,
    "password":password
}
db.demo.insert_one(doc_body)
