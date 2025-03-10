import streamlit as st
import asyncio
from main import main
from sqlalchemy import create_engine
import os
import shutil

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Create 'data' directory if it does not exist
if not os.path.exists('data'):
    os.makedirs('data')

# Ensure 'data' directory is deleted after execution
def cleanup_data_directory():
    if os.path.exists('data'):
        shutil.rmtree('data')

# Register the cleanup function to be called on exit
import atexit
atexit.register(cleanup_data_directory)

def delete_all_files_in_directory(directory: str):
    """Delete all files in the specified directory."""
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

# Set up the Streamlit app
st.title("RAG and Text-to-SQL Query In Single Interface")
st.subheader("Powered by OpenAI and Llama Cloud")

# Create a sidebar for file upload
st.sidebar.title("Upload CSV File")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

# Save the uploaded file to the 'data' directory
if uploaded_file is not None:
    delete_all_files_in_directory('data')
    with open(f"data/{uploaded_file.name}", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.sidebar.success(f"File '{uploaded_file.name}' saved to 'data' directory.")
    if 'engine' in st.session_state:
        st.session_state['engine'].dispose()
    engine = create_engine("sqlite:///:memory:", future=True)
    st.session_state['engine'] = engine
    # Reset user input when a new file is uploaded

# Accept user input
if prompt := st.chat_input("Ask Your Question Here"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Process the input and display the result
    with st.spinner("Searching using Agent..."):
        sql_query = asyncio.run(main(prompt, st.session_state['engine']))
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.success("Here is the Output:")
        st.markdown(sql_query)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": sql_query})
