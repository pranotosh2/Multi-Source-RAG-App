from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter
)
from langchain_core.documents import Document
from loader.loader import (
    load_pdf,
    load_text,
    load_web,
    clean_text,
    load_yt
)


def process_file(file_path):
    # -------- LOAD --------
    if file_path.lower().endswith(".pdf"):
        documents = load_pdf(file_path)
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )

    elif file_path.lower().endswith(".txt"):
        documents = load_text(file_path)
        splitter = CharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separator="\n"
        )

    elif file_path.lower().startswith(("http://", "https://")):
        documents = load_web(file_path)
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )
    elif file_path.lower().startswith(("https://www.youtube.com", "https://youtu.be")):
        documents = load_yt(file_path)
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )
    else:
        raise ValueError("Provided file path is not supported.")
    # -------- SPLIT --------
    split_docs = splitter.split_documents(documents)

    # -------- CLEAN --------
    cleaned_docs = []
    for doc in split_docs:
        cleaned_content = clean_text(doc.page_content)
        cleaned_docs.append(
            Document(
                page_content=cleaned_content,
                metadata=doc.metadata
            )
        )

    return cleaned_docs



#print(process_file(r"D:\LangChain\text.txt"))
# url=r"https://www.geeksforgeeks.org/machine-learning/introduction-machine-learning/"
# path=r"https://www.youtube.com/watch?v=q6kJ71tEYqM&t=3s"
# print(process_file(url))