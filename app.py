
import streamlit as st 
import os 
from langchain_core.documents import Document 
from dotenv import load_dotenv 
from qna import qna, summary, format_docs 
from process import process_file 
import tempfile
from bs4 import BeautifulSoup
st.set_page_config(
    page_title="Universal RAG App",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a professional look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        font-weight: bold;
        background-color: #4CAF50;
        color: white;
        border: none;
    }
    .stButton>button:hover {
        background-color: #45a049;
        color: white;
    }
    .sidebar-header {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Main Header
st.title("🤖 Universal Document Intelligence")
st.markdown("Extract insights, generate summaries, and ask questions from PDFs, text files, websites, and YouTube videos.")
st.markdown("---")

# Initialize session state for docs
if "docs" not in st.session_state:
    st.session_state.docs = []

# Sidebar for controls
with st.sidebar:
    st.markdown('<div class="sidebar-header">⚙️ Configuration</div>', unsafe_allow_html=True)
    source_type = st.selectbox(
        "Select Data Source",
        ["PDF", "Text", "Web Link", "YouTube Link"]
    )
    
    st.markdown("---")
    
    if source_type == "PDF":
        uploaded_file = st.file_uploader("Upload PDF Document", type=["pdf"])
        if uploaded_file and st.button("Process PDF"):
            with st.spinner("Processing PDF..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.read())
                    file_path = tmp.name
                st.session_state.docs = process_file(file_path)
                st.success(f"Successfully processed {len(st.session_state.docs)} chunks.")

    elif source_type == "Text":
        uploaded_file = st.file_uploader("Upload Text Document", type=["txt"])
        if uploaded_file and st.button("Process Text"):
            with st.spinner("Processing Text..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
                    tmp.write(uploaded_file.read())
                    file_path = tmp.name
                st.session_state.docs = process_file(file_path)
                st.success(f"Successfully processed {len(st.session_state.docs)} chunks.")

    elif source_type == "Web Link":
        url = st.text_input("Enter Website URL", placeholder="https://example.com")
        if url and st.button("Process URL"):
            if url.startswith("http"):
                with st.spinner("Loading Web Content..."):
                    st.session_state.docs = process_file(url)
                    st.success(f"Successfully processed {len(st.session_state.docs)} chunks.")
            else:
                st.error("Please enter a valid HTTP/HTTPS URL.")

    elif source_type == "YouTube Link":
        yt_url = st.text_input("Enter YouTube URL", placeholder="https://youtube.com/watch?v=...")
        if yt_url and st.button("Process Video"):
            if "youtube.com" in yt_url or "youtu.be" in yt_url:
                with st.spinner("Processing YouTube Video..."):
                    st.session_state.docs = process_file(yt_url)
                    st.success(f"Successfully processed {len(st.session_state.docs)} chunks.")
            else:
                st.error("Please enter a valid YouTube URL.")

# Main content area
if not st.session_state.docs:
    st.info("👈 Please select and process a document source from the sidebar to begin.")
else:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 Document Summary")
        st.markdown("Get a concise overview of the processed document.")
        if st.button("Generate Summary"):
            with st.spinner("Analyzing and summarizing..."):
                full_text = format_docs(st.session_state.docs)
                sum_result = summary().invoke({"context": full_text})
                st.markdown(f"> {sum_result}")

    with col2:
        st.subheader("💬 Ask Questions")
        st.markdown("Interact directly with your document content.")
        question = st.text_input("What would you like to know?", placeholder="Type your question here...")
        if question:
            with st.spinner("Searching document for answers..."):
                qa_chain = qna(st.session_state.docs)
                answer = qa_chain.invoke(question)
                st.success(answer)
