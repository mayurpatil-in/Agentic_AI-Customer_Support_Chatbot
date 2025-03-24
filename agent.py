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

    try:
        with open(DOC_FILE, "r", encoding="utf-8") as f:
            text = f.read()

        for file_info in st.session_state.uploaded_files:
            text += f"\n\n{file_info['content']}"

        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = text_splitter.split_text(text)

        vectorstore = FAISS.from_texts(docs, embeddings)
        vectorstore.save_local(VECTOR_STORE_PATH)

        st.session_state.vectorstore = vectorstore
        st.session_state.knowledge_updated = False
        return vectorstore
    except Exception as e:
        st.error(f"Error creating vectorstore: {str(e)}")
        return None
    

def whisper_transcribe(duration=5, samplerate=16000):
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
    sd.wait()
    temp_audio_file = tempfile.mktemp(suffix=".wav")
    write(temp_audio_file, samplerate, audio)

    model = whisper.load_model("base")
    result = model.transcribe(temp_audio_file)

    os.remove(temp_audio_file)
    return result["text"]

def elevenlabs_tts(text, lang="en", voice="Rachel"):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.generate(
        text=text,
        voice=voice,
        model="eleven_multilingual_v2" if lang != "en" else "eleven_monolingual_v1"
    )
    temp_audio_file = tempfile.mktemp(suffix=".mp3")
    with open(temp_audio_file, "wb") as f:
        for chunk in audio:
            f.write(chunk)
    return temp_audio_file

def extract_text_from_file(uploaded_file):
    file_content = uploaded_file.getvalue()
    file_extension = uploaded_file.name.split(".")[-1].lower()


    if file_extension == "pdf":
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as tmp_file:
                tmp_file.write(file_content)
                tmp_file_path = tmp_file.name

            doc = fitz.open(tmp_file_path)
            text = "".join(page.get_text() for page in doc)

            os.unlink(tmp_file_path)
            return text
        except Exception as e:
            st.error(f"Error extracting text from PDF: {str(e)}")
            return ""
    elif file_extension in ["txt", "md", "html"]:
        return file_content.decode("utf-8")
    else:
        st.warning(f"Unsupported file type: {file_extension}")
        return ""