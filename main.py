import streamlit as st
from pdfminer import high_level
from pathlib import Path
import pickle
import streamlit_authenticator as stauth
import os

# extract text from pdf
def extract_text(pdf_path):
    extracted_text = text = high_level.extract_text(pdf_path, "")
    return extracted_text

# get a response
def get_answer(query, pdf_text):
    answer = f'query:\n{query}\n\nextracted text:\n{pdf_text}'
    return answer

# get user information
user_info = {}
cred_path = Path(__file__).parent / "hashed_passwords.pkl"
with cred_path.open("rb") as file:
    user_info = pickle.load(file)
    
credentials = {
    "usernames":{
        user_info["usernames"][0] : {
            "name" : user_info["names"][0],
            "password" : user_info["passwords"][0]
            }         
        }
}

# get the list of pdf files
file_directory = os.path.join(Path.cwd(),"file_directory")
pdf_files = [file for file in os.listdir(file_directory) if file.endswith(".pdf")]

authenticator = stauth.Authenticate(credentials, "sample_app", "abcd", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "sidebar")

if authentication_status == False:
    st.error("Username/password is incorrect")

# the app
st.title("PDF QnA")
if authentication_status == None:
    st.warning("Please enter your username and password")
    
if authentication_status:
    # logout button
    authenticator.logout("Logout", "sidebar")
    
    # file selection dropdown menu
    selected_file = st.sidebar.selectbox("Select a PDF", pdf_files)

    # input question
    question = st.text_input("Ask a Question")

    # output
    if st.button("Ask"):
        if selected_file:
            file_path = os.path.join(file_directory, selected_file)
            pdf_text = extract_text(file_path)
            answer = get_answer(question, pdf_text)
            st.write(answer)
        else:
            st.warning("Please select a PDF.")
