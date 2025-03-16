import os
import tempfile
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import CharacterTextSplitter

from elevenlabs.client import ElevenLabs
import fitz
from deep_translator import GoogleTranslator
import whisper
import sounddevice as sd
from scipy.io.wavfile import write

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

VECTOR_STORE_DIR = "vectorstore"
DOC_FILE = "company_docs.txt"
VECTOR_STORE_PATH = os.path.join(VECTOR_STORE_DIR, "company_vectorstore")

def load_vectorstore():
    if st.session_state.vectorstore is not None:
        return st.session_state.vectorstore

    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

    if os.path.exists(VECTOR_STORE_PATH) and not st.session_state.knowledge_updated:
        try:
            vectorstore = FAISS.load_local(
                VECTOR_STORE_PATH, embeddings, allow_dangerous_deserialization=True
            )
            st.session_state.vectorstore = vectorstore
            return vectorstore
        except Exception as e:
            st.error(f"Error loading vectorstore: {str(e)}")