print("hello world")
import streamlit as st
import pandas as pd
import numpy as np
st.write("""
# My first app
Hello *world!*
""")
# st.write text, tables, data etc.
df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40],
})

st.write(df)
st.table(df)
st.dataframe(df)

dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))
st.table(dataframe)
st.dataframe(dataframe.style.highlight_max(axis=1)) # 1 row 0 col

st.line_chart(dataframe)
map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(map_data)

x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)

def helper_click():
    st.write("u clicked hehe")

st.button("hi", on_click= helper_click)

if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
       np.random.randn(20, 3),
       columns=['a', 'b', 'c'])

    chart_data

st.write("hello world")
title = st.text_input("Movie title", "Life of Brian")
st.write("The current movie title is", title)

option = st.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone"),
)

st.write("You selected:", option)

if "counter" not in st.session_state:
    st.session_state.counter = 0

st.session_state.counter += 1

st.header(f"This page has run {st.session_state.counter} times.")
st.button("Run it again")

conn = st.connection("my_database")
df = conn.query("select * from t1")
st.dataframe(df)