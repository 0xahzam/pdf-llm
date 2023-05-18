# Prereq Dependencies -- langchain, openai, streamlit, tiktoken, chromadb, pypdf, pycryptodome
# How to run? `streamlit run app.py`

# ------------------ IMPORT ------------------

# variables
from details import apikey, title, book_url, collection_name, description

# Setting up api
import os

# OpenAI as LLM Service
from langchain.llms import OpenAI

# UI interface
import streamlit as st

# Importing PDF documents
from langchain.document_loaders import PyPDFLoader

# ChromaDB as vector store
from langchain.vectorstores import Chroma

# More vector store imports
from langchain.agents.agent_toolkits import (
    create_vectorstore_agent, VectorStoreToolkit, VectorStoreInfo)


def docllm(apikey, title, pdfurl, collection_name, description):
    # -------------- SETTING UP LLM --------------

    # Setting up env key
    os.environ['OPENAI_API_KEY'] = apikey

    # Creating LLM instance
    llm = OpenAI(temperature=0.7, verbose=True)

    # ------------ DOC -> VECTOR DB --------------

    # Loading the pdf
    loader = PyPDFLoader(pdfurl)

    # Splitting pages from the doc
    pages = loader.load_and_split()

    # Loading pages into a vector db, ChromaDB in this case
    store = Chroma.from_documents(pages, collection_name=collection_name)

    # Vectore store object
    vectorstore_info = VectorStoreInfo(
        name=collection_name, description=description, vectorstore=store)

    # Converting document store into langchain toolkit
    toolkit = VectorStoreToolkit(vectorstore_info=vectorstore_info)

    # Adding toolkit to an end to end LC
    agent_exceutor = create_vectorstore_agent(
        llm=llm, toolkit=toolkit, verbose=True)

    # --------------- UI INTERFACE ---------------

    # App interface -- title and input box
    st.title(title)
    prompt = st.text_input("Enter your prompt here")

    # --------- PASSING PROMPTS + SEARCH ---------

    if prompt:
        # Passing prompt to LLM
        response = agent_exceutor.run(prompt)

        # Outputting on screen
        st.write(response)

        # Similarity search expander
        with st.expander("Document Similiarity Search"):
            search = store.similarity_search_with_score(prompt)
            st.write(search[0][0].page_content)


docllm(apikey, title, book_url, collection_name, description)
