# Customer Support Chatbot 🤖

An AI-powered customer support chatbot that provides intelligent responses based on preloaded company documents. It supports both text and voice-based interactions, multilingual translations, and document uploads to enhance knowledge retrieval.

## ✨ Features

✅ Answer user queries using company documents  
✅ Accept text and voice-based inputs  
✅ Convert speech-to-text using **Whisper** and text-to-speech using **ElevenLabs**  
✅ Translate queries and responses into multiple languages  
✅ Upload documents (PDF, TXT, MD, HTML) for knowledge enhancement  
✅ Store and retrieve information using **FAISS Vector Store**  
✅ Maintain conversation memory for context-aware responses  

## 🏗️ Project Architecture

1. **User Input Handling**  
   - Users can input queries via text or voice.  
   - Voice input is transcribed using **Whisper ASR**.  

2. **Processing the Query**  
   - If not in English, queries are translated using **Google Translator API**.  
   - The chatbot searches for relevant information in the **FAISS vector store**.  
   - **LangChain + GPT-4 Turbo** processes the query and generates a response.  

3. **Response Generation**  
   - The response is translated (if required).  
   - It is displayed in text format.  
   - If enabled, text is converted to speech using **ElevenLabs API**.  

4. **Document Upload & Knowledge Enhancement**  
   - Users can upload **PDF, TXT, MD, HTML** files.  
   - Extracted text is stored in **FAISS** for improved response accuracy.  

5. **Conversation Memory Management**  
   - The chatbot maintains session history for context-aware interactions.  

## 🔧 Technology Stack

| Component             | Tool/Library |
|----------------------|----------------|
| **Frontend UI** | Streamlit |
| **AI Model** | OpenAI GPT-4 Turbo (via LangChain) |
| **Speech-to-Text** | Whisper ASR |
| **Text-to-Speech** | ElevenLabs API |
| **Translation** | Google Translator API |
| **Vector Store** | FAISS (Facebook AI Similarity Search) |
| **Document Processing** | PyMuPDF (fitz) |
| **Environment Management** | dotenv |
| **Audio Recording** | sounddevice, scipy.io.wavfile |

## 🔄 Flow Diagram

```plaintext
+-------------------------+
|      User Input         |
|  (Text / Voice Query)   |
+-----------+-------------+
            |
            v
+-------------------------+
|   Speech-to-Text (ASR)  |
|      Whisper Model      |
+-------------------------+
            |
            v
+-------------------------+
|   Language Detection    |
|   & Translation (API)   |
+-------------------------+
            |
            v
+-------------------------+
|  Query Understanding    |
|   (LangChain + GPT-4)   |
+-------------------------+
            |
            v
+-------------------------+
|  Knowledge Retrieval    |
|  (FAISS Vector Store)   |
+-------------------------+
            |
            v
+-------------------------+
|  Generate Response      |
|   (LangChain + GPT-4)   |
+-------------------------+
            |
            v
+-------------------------+
|  Translate Response     |
|   (Google Translator)   |
+-------------------------+
            |
            v
+-------------------------+     +-----------------------+
|  Display Response       |     |  Text-to-Speech (TTS) |
|  (Streamlit UI)         | <-- |   ElevenLabs API      |
+-------------------------+     +-----------------------+
```


# How It Works (Step-by-Step Flow)

## 1️⃣ User Provides Input
- If **text**, it is directly processed.  
- If **voice**, it is recorded and transcribed by **Whisper AI**.  

## 2️⃣ Language Detection & Translation
- If the query is not in English, it is translated using **Google Translator**.  

## 3️⃣ Query Processing & AI Response
- The chatbot fetches relevant context from **FAISS Vector Store**.  
- Uses **GPT-4 Turbo (LangChain)** to generate an answer.  

## 4️⃣ Response Translation (If Needed)
- If the user's preferred language is not English, the response is translated.  

## 5️⃣ Output Response to the User
- **Text response** appears in the chat window.  
- **Audio response** (optional) is generated via **ElevenLabs API**.  

## 6️⃣ Maintain Conversation History
- The system keeps track of user queries for **context-aware interactions**.  

## 7️⃣ Document Upload & Knowledge Updates
- Users can upload **PDF/TXT/MD/HTML** files.  
- Extracted text is stored in **FAISS Vector Store** for future queries.  


