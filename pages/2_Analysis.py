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
from datetime import date

#st.subheader('Feed me with your excel file')
#columns=st.session_state["columns"]


if "uploaded_file" not in st.session_state:
    st.session_state["uploaded_file"]=""
st.subheader("Upload the visualization template file")
uploaded_file = st.file_uploader('Upload the file',type = 'csv')

if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.session_state["uploaded_file"]=df

        col = (df.shape[1])-7
        columns = []
        for i in range(col):
            columns.append('Q' + str(i+1))


        df = df.replace(['-'], 'absent')
        df = df.replace(['null'], 'zero')
        option = st.selectbox(
            'What do you like to analyse?',
            ('Student with low score', 'Concept with less understanding', 'Cognitive level','Total mark of student')
            )

       
        if option == "Total mark of student":
            top_10 = df['Score'].value_counts()
            st.bar_chart(top_10)
            plt.title('Total marks of the students')
            plt.xlabel('Scores')
            plt.ylabel('Student Count')
        elif option == "Student with low score":
            #n=st.session_state["ques"]
            n=col
            df2=df
            df2=df2.sort_values('First name')
            fig = plt.figure(figsize=(20,10))
            ax = fig.add_subplot(1,1,1)
            x = np.arange(1, 42, 1)
            plt.xticks(x)
            plt.grid()
            ax.scatter(
            df2["First name"],
            df2["Correct"],
            cmap='jet'
    )
            x=df2["First name"]
            y=df2["Correct"]


            def pltcolor(lst):
             cols=[]
             m=(n*40)/100
             for l in lst:
                   if l<=m:
                    cols.append('red')
                  
                   else:
                    cols.append('green')
             return cols

            cols=pltcolor(y)

            plt.scatter(x=x,y=y,s=250,c=cols) 
            plt.grid(True)
            plt.show()
            df2.plot.scatter('First name', 'Correct', c='Correct', colormap='jet')
            ax.set_xlabel("Card number")
            ax.set_ylabel("Correct")
            st.write(fig)
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
            st.markdown("<h4 style='text-align: center; color: white;'>Attention required Students</h4>",  unsafe_allow_html=True)
            st.table(dff)
            
            df2 = df2.replace(['absent','<NA>'], 0)
         
            df2['Score'] = df2['Score'].map(lambda x: str(x).rstrip('%')).astype(float)
            
            bins = [0,40,50,60,70,80,90,100]
            group_names=['1-40','41-50','51-60','61-70','71-80','81-90','91-100']
            
            top_10 = pd.cut(df2['Score'],bins=bins,labels=group_names)
            st.markdown("<h4 style='text-align: center; color: white;'> Categorization of students based on scores</h4>",  unsafe_allow_html=True)
            fig = px.pie(top_10, names='Score')
            st.write(fig)
    
        elif option == "Concept with less understanding":
            st.write("You selected Difficult questions ")
            df3=pd.DataFrame()
            for i in columns:
                a=df[i][1]
                df2=df
                df = df.iloc[2:]
                df["Diff"] = np.where((df[i]!=a),"Incorrect","Correct")
                df3[i]=df["Diff"]
                df=df2
            fig = plt.figure(figsize=(10, 4))
            ax=sns.countplot(x="variable", hue="value", data=pd.melt(df3),palette=['#432371',"#FAAE7B"])
            ax.set(xlabel="Questions",ylabel="Count")
            st.pyplot(fig) 
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
                    

        elif option == "Cognitive level":
            st.write("You selected Cognitive level")
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
            option = st.selectbox(
                'What do you like to analyse?',
             ('Individual student','Entire class')
        )
            if option=="Individual student":
                card_no=df['First name'].sort_values()
                card_no.dropna(inplace=True)
                card_choice= st.selectbox('', card_no)
                st.write("You have selected:",card_choice)
                score1=0
                score2=0
                low=0
                high=0
                score_fin1=0
                score_fin2=0
                for i in col1:
                    c=df3.loc[df3['First name'] == card_choice,i]
                    a=df3[i][1]
                    e = np.where(c==a , score1+1 ,score1+0)
                    score_fin1=score_fin1+e
                for j in col2:
                    d=df4.loc[df4['First name'] == card_choice,j]
                    b=df4[j][1]
                    f= np.where(b==d , score2+1 ,score2+0)
                    score_fin2=score_fin2+f
        
                low=(score_fin1/n)*100
                high=(score_fin2/m)*100

                st.write("The score in lower cognitive level is:",low[0],"%")
                st.write("The score in higher cognitive level is:",high[0],"%")
            
                from plotly.subplots import make_subplots
                trace1 = go.Indicator(mode="gauge+number",    value=low[0],    domain={'row' : 1, 'column' : 1}, title={'text': "Low cognitive"}, gauge = {'axis': {'range': [None, 100]},
                 'steps' : [
                 {'range': [0, 250], 'color': "lightgray"},
                 {'range': [250, 400], 'color': "gray"}],
             })
                trace2 = go.Indicator(mode="gauge+number",    value=high[0],    domain={'row' : 1, 'column' : 2}, title={'text': "High cognitive"}, gauge = {'axis': {'range': [None, 100]},
             'steps' : [
                 {'range': [0, 250], 'color': "lightgray"},
                 {'range': [250, 400], 'color': "gray"}],
             })
                fig = make_subplots(
                rows=1,
                cols=2,
                specs=[[{'type' : 'indicator'}, {'type' : 'indicator'}]],
            )
                fig.append_trace(trace1, row=1, col=1)
                fig.append_trace(trace2, row=1, col=2)
                st.write(fig)
            elif option=="Entire class":
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

                st.write("The score in lower cognitive level is:",lower[0],"%")
                st.write("The score in higher cognitive level is:",higher[0],"%")

                import plotly.graph_objs as go
                from plotly.subplots import make_subplots
                trace1 = go.Indicator(mode="gauge+number",    value=lower[0],    domain={'row' : 1, 'column' : 1}, title={'text': "Low cognitive"},gauge = {'axis': {'range': [None, 100]},
                  'steps' : [
                 {'range': [0, 250], 'color': "lightgray"},
                 {'range': [250, 400], 'color': "gray"}],
             })
                trace2 = go.Indicator(mode="gauge+number",    value=higher[0],    domain={'row' : 1, 'column' : 2}, title={'text': "High cognitive"},gauge = {'axis': {'range': [None, 100]},
             'steps' : [
                 {'range': [0, 250], 'color': "lightgray"},
                 {'range': [250, 400], 'color': "gray"}],
             })
                fig = make_subplots(
                rows=1,
                cols=2,
                specs=[[{'type' : 'indicator'}, {'type' : 'indicator'}]],
            )
                fig.append_trace(trace1, row=1, col=1)
                fig.append_trace(trace2, row=1, col=2)
                st.write(fig)
        
        client = MongoClient('mongodb+srv://student:visualization@cluster0.phhdmbo.mongodb.net/?retryWrites=true&w=majority')
        db = client['Excel']

        def gio():
         try:  
             curr_date= st.session_state["date"]
             curr_date=curr_date.strftime("%d/%m/%y")
             name = str(curr_date)   
             collect=db.create_collection(name)
             collect.insert_many(df.to_dict('records'))
             st.write(collect)
         except:
             y=0
        gio()
