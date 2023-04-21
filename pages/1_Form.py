import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import plotly.express as px
import plotly.graph_objects as go
import datetime
from pymongo import MongoClient

st.set_page_config(page_title='Excel Plotie',layout = "wide")

if 'username' not in st.session_state:
       st.session_state.username = ''

if st.session_state.username != '':
    c1,c2,c3=st.columns((0.1,0.1,0.05))
    with c3:
        def user_update(name):
            st.session_state.username = name

        my_expander = st.expander(st.session_state.username, expanded=True)
        with my_expander:
            logout = st.button(label='Log Out')
            if logout:
                    user_update('')
                    st.session_state.form = ''
        
    st.title('FORM 📝')


    first_column = [""]
    second_column = [""]
    third_column = [""]
    fourth_column = [""]
    fifth_column = [""]
    def load_data():
                return pd.DataFrame(
            {
                "Card number":first_column,
                "First name":second_column,
                "Score" : third_column,
                "Correct": fourth_column,
                "Answered": fifth_column,
            }
        )
    df5= load_data()
    questions = ["Q1","Q2","Q3","Q4","Q5","Q6","Q7","Q8","Q9","Q10","Q11","Q12","Q13","Q14","Q15","Q16","Q17","Q18","Q19","Q20"]
    columns=[]
    if "columns" not in st.session_state:
        st.session_state["columns"]=""
    if "ques" not in st.session_state:
        st.session_state["ques"]=""
    if "date" not in st.session_state:
        st.session_state["date"]=""

        
    with st.form("my-form"):
        st.subheader("Fill the form with the number of questions,date and topic and click submit")
        curr_date= st.date_input("Enter Date (YYYY/MM/DD)")
        st.session_state["date"]=curr_date
        ques = st.number_input('Enter the no of questions', min_value=1, max_value=20, value=1, step=0)
        st.session_state["ques"]=ques
        topic = st.text_input('Topic name')
        st.session_state["topic"]=topic
        submit = st.form_submit_button("Submit")
        df5['Card number'][0]= topic
    with st.form("Excel_form"):
            st.subheader("Choose the Blooms taxonomy levels for each question and click submit")
            var = 0
            for i in range(0,ques):
                    st.write(questions[var])
                    columns.append(questions[var])
                    #st.write(st.session_state["columns"[var]])
                    genre = st.radio ("Select the cognitive level",
                    ('Remember', 'Understand', 'Analyse', 'Apply'),key=i)
                    df5[questions[var]]=""
                    df5[questions[var]][0]=genre
                    var = var + 1
            submit = st.form_submit_button("Submit")
            
    st.session_state["columns"]=columns

    #if submit:
        #get_data().append({"No of questions": ques})

    st.write(df5)
    @st.cache
    def convert_df(df):
        return df.to_csv().encode('utf-8')

    csv = convert_df(df5)
    st.subheader("Download the data and fill the details as shown in the below image teamplate.")
    st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='visualization_template.csv',
            mime='text/csv',
    )

    client =  MongoClient('mongodb+srv://student:visualization@cluster0.phhdmbo.mongodb.net/?retryWrites=true&w=majority')
    db = client['Excel']
    doc_body={
        "topic":topic
    }
    db.demo.insert_one(doc_body)

    import streamlit as st
    from PIL import Image

    image = Image.open('template.jpeg')

    st.image(image, caption='Sample Template')

    

else:
      st.write("You don't have access !!! Please Login and continue")
