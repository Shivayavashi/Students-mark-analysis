import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from pymongo import MongoClient
import csv
from datetime import datetime

client = MongoClient('mongodb+srv://student:visualization@cluster0.phhdmbo.mongodb.net/?retryWrites=true&w=majority')
db = client['Excel']

t = st.sidebar.selectbox(
    'What do you like to analyse?',
    ('Topic wise', 'Date wise')
)


def load_mongo_data(coll_name):
    a = db[coll_name]
    data = pd.DataFrame.from_records(a.find())


if t == 'Date wise':
    lists = db.list_collection_names()
    lists.remove("demo")
    sorted_dates = sorted(
        lists, key=lambda d: datetime.strptime(d, '%d/%m/%y'))

    lists = sorted_dates
    
    coll_name_1 = st.sidebar.selectbox(
        "Select from collection: ", lists)
    load_mongo_data(coll_name_1)
    coll_name_2 = st.sidebar.selectbox(
        "Select to collection: ", lists)
    load_mongo_data(coll_name_2)
    r = []
    data = {}
    list1 = []
    list1.append(coll_name_1)
    list1.extend(lists[lists.index(coll_name_1)+1:lists.index(coll_name_2)])
    list1.append(coll_name_2)

    r = list1
    col_count = []
    var = []

    for j in r:
        collection = db[j]
        data[j] = pd.DataFrame(list(collection.find()))

        col_count.append((data[j].shape[1])-7)
        data[j]['Score'] = data[j]['Score'].replace(['absent', '<NA>'], 0)
        data[j]['Score'] = data[j]['Score'].map(
            lambda x: str(x).rstrip('%')).astype(float)
        m = data[j]['Score'].sum()
        n = (m/40)
        var.append(n)

    option = st.selectbox(
        'What do you like to analyse?',
        ('Overall performance', 'Cognitive level performance over the week',
         'Individual overall performance')
    )

    if option == 'Overall performance':
        chart_data = pd.DataFrame(var, r)
        fig = px.line(chart_data)

        fig.update_layout(
            title="Overall performance",
            xaxis_title="Date",
            yaxis_title="Performance score",
            legend_title="Score",
            font=dict(
                family="Courier New, monospace",
                size=20,
            )
        )
        st.write(fig)
    
    elif option == 'Individual overall performance':
        st.write("Select the Roll no")
        card_no = data[j]['First name'].sort_values()
        card_no.dropna(inplace=True)
        card_choice = st.selectbox('', card_no)
        st.write("You have selected:", card_choice)
        a = []
        for j in r:
            c = data[j].loc[data[j]['First name'] == card_choice, 'Score']
            a.append(c)
        chart_data=pd.DataFrame(a,r)
        st.area_chart(chart_data)

    elif option == 'Cognitive level performance over the week':
        s = []
        h = []
        for j in r:
            st.write(j)
            df3 = pd.DataFrame()
            df4 = pd.DataFrame()
            n = 0
            m = 0
            df3["First name"] = data[j]["First name"]
            df4["First name"] = data[j]["First name"]
            columns = (data[j].shape[1])-7
            st.write(columns)
            b = []
            for i in range(columns):
                b.append('Q' + str(i+1))

            for i in b:
                a = data[j][i][0]
                if (a == "Remember"):
                    df3[i] = data[j][i]
                    n = n+1
                elif (a == "Understand"):
                    df3[i] = data[j][i]
                    n = n+1
                elif (a == "Apply"):
                    df4[i] = data[j][i]
                    m = m+1
                elif (a == "Analyse"):
                    df4[i] = data[j][i]
                    m = m+1
            st.write(m)
            st.write(n)
            col1 = []
            col2 = []
            col1 = df3.columns[1:]
            col2 = df4.columns[1:]
            arr = np.array(data[j]["First name"])
            score1 = 0
            score2 = 0
            score_fin1 = 0
            score_fin2 = 0

            for i in col1:
                for k in range(2, 42):
                    c = df3.loc[df3['First name'] == arr[k], i]
                    a = df3[i][1]
                    e = np.where(c == a, score1+1, score1+0)
                    score_fin1 = score_fin1+e

            for j in col2:
                for k in range(2, 42):
                    d = df4.loc[df4['First name'] == arr[k], j]
                    b = df4[j][1]
                    f = np.where(b == d, score2+1, score2+0)
                    score_fin2 = score_fin2+f
            st.write(score_fin1)
            st.write(n)
            lower = (score_fin1/(n*40))*100
            higher = (score_fin2/(m*40))*100

            s.append(lower[0])
            h.append(higher[0])

            st.write("The score in lower cognitive level is:", lower[0], "%")
            st.write("The score in higher cognitive level is:", higher[0], "%")

        import numpy as np
        import matplotlib.pyplot as plt

        X_axis = np.arange(len(r))
        fig = plt.figure(figsize=(10, 5))
        plt.bar(X_axis - 0.2, s, 0.4, label='lower cognitive', color='#432371')
        plt.bar(X_axis + 0.2, h, 0.4, label='higher cognitive', color='#FAAE7B')

        plt.xticks(X_axis, r)
        plt.xlabel("Date")
        plt.ylabel("Cognitive performance")
        plt.title("Cognitive level performance over the week")
        plt.legend()

        st.write(fig)
        plt.show()

elif t == 'Topic wise':
    var = []
    f = []
    col_count = []
    topic = []
    mark = []
    col = db['demo']
    documents = list(col.find())
    for doc in documents:
        var.append(doc["topic"])
    f.extend(list(set(var)))
    options = st.multiselect(
    'Select the topic',f)
    lists = db.list_collection_names()
    lists.remove("demo")
   
    data = {}
    data1 = {}
    k = 0
    for j in lists:
        collection = db[j]
        data[j] = pd.DataFrame.from_records((collection.find()))
        if (data[j]['Card number'][0]) in options:
            data1[k] = data[j]
            k = k + 1
            col_count.append((data[j].shape[1])-7)
            data[j]['Score'] = data[j]['Score'].replace(['absent', '<NA>'], 0)
            data[j]['Score'] = data[j]['Score'].map(
            lambda x: str(x).rstrip('%')).astype(float)
            m = data[j]['Score'].sum()
            n = (m/40)
            mark.append(n)
            topic.append(data[j]['Card number'][0])
  
   

#Zip the two lists together, and create a dictionary out of the zipped lists
    from collections import defaultdict

    my_dict = defaultdict(list)
    dict = []
    for k, v in zip(topic,mark):
        my_dict[k].append(v)
    for new_k, new_val in my_dict.items():
        dict = ({k:sum(v)/len(v)} for k, v in my_dict.items())

    df = pd.DataFrame(
    {'Topic': topic, 'Score': mark})
    dff = df.groupby("Topic").Score.mean().reset_index()
    st.markdown("<h4 style='text-align: center; color: white;'>TOPIC PERCENT OUT OF 100</h4>",  unsafe_allow_html=True)
    import plotly.express as px
    fig = px.bar_polar(dff, r="Score", theta="Topic",
                   color="Score", template="plotly_dark",
                   color_discrete_sequence= px.colors.sequential.Plasma_r)
    st.write(fig)
    fig=px.bar(dff,x='Score',y='Topic', orientation='h',color='Topic',color_discrete_sequence=px.colors.qualitative.Set3)
    st.write(fig)
