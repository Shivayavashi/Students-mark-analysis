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
import plost
from PIL import Image
from fpdf import FPDF
import plotly.io as pio
figs = []


@st.experimental_singleton(suppress_st_warning=True)
def init_connection():
    return MongoClient("mongodb+srv://st.secrets.DB_USERNAME:st.secrets.DB_PASSWORD@cluster0.phhdmbo.mongodb.net/?retryWrites=true&w=majority")
st.set_page_config(layout="wide")

client = init_connection()
db = client.Excel


@st.experimental_memo(ttl=600)
def get_data():
    items = db.demo.find()
    items = list(items)  # make hashable for st.experimental_memo
    return items

items = get_data()

# Print results.
for item in items:
    st.write(f"{item['id']} has a :{item['time']}:")
    
    
def load_mongo_data(coll_name):
    a = db[coll_name]
    data = pd.DataFrame.from_records(a.find())
    return data
   
lists = db.list_collection_names()
lists.remove("demo")
sorted_dates = sorted(
        lists, key=lambda d: datetime.strptime(d, '%d/%m/%y'))

lists = sorted_dates
option = st.sidebar.selectbox('Select the date',sorted_dates)
data1 = load_mongo_data(option)

col = (data1.shape[1])-7
columns = []
for i in range(col):
    columns.append('Q' + str(i+1))
a1,a2=st.columns((0.2,0.1))
c2,c3=st.columns((0.1,0.1))


with c2:
    st.markdown("<h4 style='text-align: center; color: white;'>Cognitive percentage</h4>",  unsafe_allow_html=True)
    df=data1
    df3=pd.DataFrame()
    df4=pd.DataFrame()
    n=0
    m=0
    df3["First name"]=df["First name"]
    df4["First name"]=df["First name"]
    for i in columns:
        a=df[i][0]
        if (a=="Remember"):
            df3[i]=df[i]
            n=n+1
        elif (a=="Understand"):
            df3[i]=df[i]
            n=n+1
        elif (a == "Apply"):
            df4[i]=df[i]
            m=m+1
        elif (a=="Analyse"):
            df4[i]=df[i]
            m=m+1
            #st.dataframe(df.sort_values(by="First name"))
    col1=[]
    col2=[]
    col1=df3.columns[1:]
    col2=df4.columns[1:]
    arr=np.array(df["First name"])
    score1=0
    score2=0
    low=0
    high=0
    col1=[]
    col2=[]
    col1=df3.columns[1:]
    col2=df4.columns[1:]
    score_fin1=0
    score_fin2=0
    for i in col1:
        for k in range(2,42):
            c=df3.loc[df3['First name'] == arr[k],i]
            a=df3[i][1]
            e = np.where(c==a , score1+1 ,score1+0)
            score_fin1=score_fin1+e          
        
    for j in col2:
        for k in range(2,42):
            d=df4.loc[df4['First name'] == arr[k],j]
            b=df4[j][1]
            f= np.where(b==d , score2+1 ,score2+0)
            score_fin2=score_fin2+f
    lower=(score_fin1/(n*40))*100
    higher=(score_fin2/(m*40))*100


    import plotly.graph_objs as go
    from plotly.subplots import make_subplots
    trace1 = go.Indicator(mode="gauge+number",    value=lower[0],    domain={'row' : 1, 'column' : 1}, title={'text': "Low cognitive"},gauge = {'axis': {'range': [None, 100]},
                    'steps' : [
                    {'range': [0, 100], 'color': "lightgray"},
                    {'range': [100, 200], 'color': "gray"}],
                })
    trace2 = go.Indicator(mode="gauge+number",    value=higher[0],    domain={'row' : 1, 'column' : 2}, title={'text': "High cognitive"},gauge = {'axis': {'range': [None, 100]},
                'steps' : [
                    {'range': [0, 100], 'color': "lightgray"},
                    {'range': [100, 200], 'color': "gray"}],
                })
    fig = make_subplots(
    rows=1,
    cols=2,
    specs=[[{'type' : 'indicator'}, {'type' : 'indicator'}]],
    )
    fig.append_trace(trace1, row=1, col=1)
    fig.append_trace(trace2, row=1, col=2)
    fig.update_layout(width=550)
    st.write(fig)

with a2:
        
        st.markdown("<h4 style='text-align: center; color: white;'>Scores pie</h4>",  unsafe_allow_html=True)
        df2 = data1.replace(['absent','<NA>'], 0)
        df2['Score'] = df2['Score'].map(lambda x: str(x).rstrip('%')).astype(float) 
        bins = [0,40,50,60,70,80,90,100]
        group_names=['1-40','41-50','51-60','61-70','71-80','81-90','91-100']
        top_10 = pd.cut(df2['Score'],bins=bins,labels=group_names)
        fig = px.pie(top_10, names='Score')
        #fig.update_layout(margin=dict(t=10, b=10, l=10, r=10))
        fig.update_layout(width=400)
        st.write(fig)
       


with a1:
    st.markdown("<h4 style='text-align: center; color: white;'>Scores bar</h4>",  unsafe_allow_html=True)
    top_10 = data1['Correct'].value_counts()
    state_total_graph = px.bar(
        top_10,
        color=top_10)
    state_total_graph.update_layout(
    title="Scores of Students",
    xaxis_title="Scores",
    yaxis_title="Number of students",
    legend_title="Score",
)
    st.plotly_chart(state_total_graph)
    

with c3:
            df3=pd.DataFrame()
            for i in columns:
                a=df[i][1]
                df2=df
                df = df.iloc[2:]
                df["Diff"] = np.where((df[i]!=a),"Incorrect","Correct")
                df3[i]=df["Diff"]
                df=df2
            #fig = plt.figure(figsize=(10, 4))
            #sns.set_style(style=None)
            #ax=sns.countplot(x="variable", hue="value", data=pd.melt(df3),palette=['#432371',"#FAAE7B"])
            #ax.set(xlabel="Questions",ylabel="Count")
            #ax.set_facecolor('white')
            #st.write(fig)
            
            df_plot = pd.melt(df3)
            df_plot = df_plot.groupby(by=["variable","value"]).size().reset_index(name="counts")
            fig=px.bar(data_frame=df_plot, x="variable", y="counts", color="value", barmode="group",  color_discrete_map={
        'Correct': 'white',
        'Incorrect': 'green'
    })
            st.markdown("<h4 style='text-align: center; color: white;'>Question wise analysis</h4>",  unsafe_allow_html=True)
            fig.update_layout(
    xaxis_title_text='Questions', 
    yaxis_title_text='Count',
    bargap=0.2, # gap between bars of adjacent location coordinates
    bargroupgap=0.1 # gap between bars of the same location coordinates
)
            #fig = px.bar(df_plot, x='variable', y='value', color='variable', barmode='group')
            #fig=px.histogram(pd.melt(df3), x='variable', color="variable", barmode='group')
            #fig=px.bar(df3, x='variable', y='value',
             #color='variable',
             #height=400)
            import time
            fig.update_layout(width=600)
            st.write(fig)
            ab=0
            k=0
            for i in columns:
                if(df3[i].value_counts()['Incorrect']>df3[i].value_counts()['Correct']):
                    ab = i
                    k=k+1
                    value=ab+" - "+df[i][0]
                    st.markdown("<h6 style='text-align: center; color: white;'>"+value+"</h6>",  unsafe_allow_html=True)
            if(k!=0):
                st.markdown("<h6 style='text-align: center; color: white;'>Require more attention !!!</h6>",  unsafe_allow_html=True)
                    
            
st.text('\n')  
st.text('\n')       
import plotly.express as px
n=col
df2=data1
df2=df2.sort_values('First name')
st.markdown("<h4 style='text-align: center; color: white;'>Student Scores</h4>",  unsafe_allow_html=True)
fig = go.Figure(go.Scatter(mode="markers", x=df['First name'], y=df['Correct'],
marker_symbol='circle',marker_line_color="midnightblue", marker_color=df['Correct'],marker_line_width=2, marker_size=15))
fig.update_layout(width=1024, height=500)
fig.update_layout(
   xaxis = dict(
      tickmode = 'linear',
      tick0 = 1,
      dtick = 1,
      title='Card number'
   ),
    yaxis = dict(
      title='Scores'
   )
)
st.write(fig)

d1,d2,d3=st.columns((3))
with d2:

    dff=pd.DataFrame()
    first_column=[""]
    second_column=[""]
                #n=st.session_state["ques"]
    n=col
    num=n*40/100
    for i in range(0,40):
        a=df['Correct'][i]
        b=df['Answered'][i]
        if (a<= num):
            if(b!=0):
                first_column.append(df['First name'][i])
                second_column.append(df['Correct'][i])
                
    def load_data():
        return pd.DataFrame(
            {
                "Card no":first_column,
                "No of correct":second_column,
            }
        )
    dff = load_data()
    st.text('\n')  
    st.text('\n')
    st.markdown("<h4 style='text-align: center; color: white;'>Student with low scores</h4>",  unsafe_allow_html=True)
    dff.drop(index=df.index[0], axis=0, inplace=True)
    #dff=dff.sort_values(by=['No of correct'])
    st.table(dff)
