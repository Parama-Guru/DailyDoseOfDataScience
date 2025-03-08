import streamlit as st
import asyncio
from main import main

# Set up the Streamlit app
st.title("Text to SQL Converter")
st.subheader("Transform your text into SQL queries effortlessly")

# User input section
user_input = st.text_input("Enter your text here:", placeholder="Type something...")

# Process the input and display the result
if user_input:
    with st.spinner("Generating SQL query..."):
        sql_query = asyncio.run(main(user_input))
    st.success("Here is the generated SQL query:")
    st.code(sql_query, language='sql')
