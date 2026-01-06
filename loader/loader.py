
import os
import re
import unicodedata
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    WebBaseLoader
)
from langchain_core.documents import Document
from youtube_transcript_api import YouTubeTranscriptApi


def load_pdf(file_path):
    loader=PyPDFLoader(file_path)
    docs=loader.load()
    return docs


def load_text(file_path):
    loader=TextLoader(file_path)
    docs=loader.load()
    return docs

def load_web(url):
    loader=WebBaseLoader(url)
    docs=loader.load()
    return docs

def load_yt(url):
    match = re.search(r"(?:v=|youtu\.be/|embed/)([\w-]{11})", url)
    video_id= match.group(1)
    ytt_api = YouTubeTranscriptApi()
    transcript_list=ytt_api.fetch(video_id)
    transcript = " ".join(chunk.text for chunk in transcript_list)
    return transcript
    


def clean_text(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).lower()

    # Remove urls, emails
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"\S+@\S+", " ", text)

    # Remove timestamps & page refs
    text = re.sub(r"\b\d{1,2}:\d{2}(:\d{2})?\b", " ", text)
    text = re.sub(r"\bpage\s+\d+\b", " ", text)

    # Remove spoken fillers (youtube friendly)
    text = re.sub(r"\b(uh|um|you know|like|okay|right)\b", " ", text)

    # Remove special chars
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # Normalize spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


#path=r"D:\LangChain\text.txt"
#path=r"D:\LangChain\Commonly Asked ML Interview Questions and Answers.pdf"
# url=r"https://www.geeksforgeeks.org/machine-learning/introduction-machine-learning/"
# path=r"https://www.youtube.com/watch?v=q6kJ71tEYqM&t=3s"

# document=load_web(url)
# docs=[]
# for doc in document:
#     cleaned_content = clean_text(doc.page_content)
#     docs.append(cleaned_content)
# print(f"Cleaned {len(docs)} pages.")
# print(docs)

# print(load_yt(path))