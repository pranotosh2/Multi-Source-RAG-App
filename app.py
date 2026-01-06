
import streamlit as st 
import os 
from langchain_core.documents import Document 
import base64 
from dotenv import load_dotenv 
from qna import qna, summary,format_docs 
from process import process_file 
import tempfile

st.set_page_config(
    page_title="Universal RAG App",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Universal Document Q&A & Summary")
st.write("Upload PDF / TXT / Web-Link / YouTube-link")

# ---------------- SOURCE SELECTION ----------------
source_type = st.selectbox(
    "Select source type",
    ["PDF", "Text", "Web Link", "YouTube Link"]
)

docs = []

# ---------------- PDF ----------------
if source_type == "PDF":
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            file_path = tmp.name

        with st.spinner("Processing PDF..."):
            docs = process_file(file_path)

        st.success(f"📄 Processed {len(docs)} chunks from PDF")


# ---------------- TEXT ----------------
elif source_type == "Text":
    uploaded_file = st.file_uploader("Upload Text File", type=["txt"])

    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
            tmp.write(uploaded_file.read())
            file_path = tmp.name

        with st.spinner("Processing Text..."):
            docs = process_file(file_path)

        st.success(f"📝 Processed {len(docs)} chunks from Text file")


# ---------------- WEB ----------------
elif source_type == "Web Link":
    url = st.text_input("Paste website URL")

    if url:
        if url.startswith("http"):
            with st.spinner("Loading web content..."):
                docs = process_file(url)

            st.success(f"🌐 Processed {len(docs)} chunks from Web page")
        else:
            st.error("❌ Please enter a valid website URL")


# ---------------- YOUTUBE ----------------
elif source_type == "YouTube Link":
    yt_url = st.text_input("Paste YouTube URL")

    if yt_url:
        if "youtube.com" in yt_url or "youtu.be" in yt_url:
            with st.spinner("Processing YouTube video..."):
                docs = process_file(yt_url)

            st.success(f"🎥 Processed {len(docs)} chunks from YouTube video")
        else:
            st.error("❌ Invalid YouTube URL")


        

# ---------------- SUMMARY ----------------
if st.button("📘 Generate Summary"):
    if not docs:
        st.warning("Please provide a document first")
    else:
        with st.spinner("Summarizing..."):
            full_text = format_docs(docs)
            summary = summary().invoke({"context": full_text})

        st.subheader("📄 Summary")
        st.write(summary)

st.markdown("---")

# ---------------- Q&A ----------------
question = st.text_input("Ask a question")

if question:
    if not docs:
        st.warning("Please provide a document first")
    else:
        with st.spinner("Generating answer..."):
            qa_chain = qna(docs)
            answer = qa_chain.invoke(question)

        st.subheader("💡 Answer")
        st.write(answer)



