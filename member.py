import streamlit as st
from pathlib import Path
import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
import openai
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.vectorstores import FAISS 


# extract text from pdf
def extract_text(pdf_path):
    # extracted_text = text = high_level.extract_text(pdf_path, "")
    doc_reader = PdfReader(pdf_path)
    raw_text = ""
    for page in doc_reader.pages:
        raw_text += page.extract_text()
    # raw_text = raw_text.replace(' ', '')
    # raw_text = raw_text.replace('\n', ' ')
    return raw_text

# get a response
def get_answer(query, pdf_text):
    answer = f'query:\n{query}\n\nextracted text:\n{pdf_text}'
    return answer

# get the list of pdf files
file_directory = os.path.join(Path.cwd(),"file_directory")
pdf_files = [f'sample{i}.pdf' for i in range(1, len(os.listdir(file_directory))+1)]

def member_page():
    st.title("PDF - QnA")
    
    # file selection dropdown menu
    selected_file = st.selectbox("Select a PDF", pdf_files)

    ### OpenAI API Key
    load_dotenv()
    api = os.getenv("openai_api_key")
    os.environ["OPENAI_API_KEY"] = api

    # input question
    question = st.text_input("Ask a Question")

    # output
    if st.button("Ask"):
        if selected_file:
            file_path = os.path.join(file_directory, selected_file)
            pdf_text = extract_text(file_path)

            ### GenerativeAI

            splitter = CharacterTextSplitter(
            separator = ".",
            chunk_size = 200,
            chunk_overlap = 100,
            length_function = len
            )
            chunk_lst = splitter.split_text(pdf_text)

            embeddings = HuggingFaceEmbeddings()
            doc_search = FAISS.from_texts(chunk_lst, embeddings)

            chain = load_qa_chain(OpenAI(), 
                            chain_type="stuff") 
            

            query = question
            docs = doc_search.similarity_search(query)
            op = chain.run(input_documents=docs, question=query)
            
            st.write(op)
        else:
            st.warning("Please select a PDF.")