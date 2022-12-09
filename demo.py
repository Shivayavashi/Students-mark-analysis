import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Excel Plotie')
st.title('Excel Plotie 👾')
st.subheader('Feed me with your excel file')

uploaded_file = st.file_uploader('choose a file',type = 'csv')
if uploaded_file:
    st.markdown('......')
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)
    groupby_column = st.selectbox(
        'what would you like to analyze?', 
        ('Score','Correct'),
    )

    output_column = ['Score']
    df_grouped = df.groupby(by=[groupby_column],as_index=False)[output_column].count()

    fig = px.bar(
        df_grouped,
        x=groupby_column,
        y='Correct',
        color='Score',
        color_continuous_scale=['red','yellow','green'],
        template='plotly_white',
        title=f'<b>Score and Correct by {groupby_column}</b>'
    )
    st.plotly_chart(fig)