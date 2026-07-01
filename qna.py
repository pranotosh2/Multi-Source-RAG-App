from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.documents import Document
from process import process_file
from langchain_groq import ChatGroq
from embeddings.embedding import get_embeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnableLambda, RunnablePassthrough
from langchain_community.vectorstores import FAISS
import os
load_dotenv()


# llm = HuggingFaceEndpoint(
#     repo_id="deepseek-ai/DeepSeek-R1",
#     task="text-generation",
#     #max_new_tokens=700,
#     temperature=0.7     
# )

model = ChatGroq(
    temperature=0, 
    model_name="openai/gpt-oss-120b", # Updated to a supported Llama 3 model on Groq
    api_key=os.environ.get("GROQ_API_KEY", "dummy_key") # will fail on run if not set
)

def format_docs(docs):
  context_text = "\n\n".join(doc.page_content for doc in docs)
  return context_text

def qna(docs):
    embeddings=get_embeddings()
    vector_store=FAISS.from_documents(docs, embeddings)
    retriever=vector_store.as_retriever(search_type="similarity", search_kwargs={"k":5})
    prompt=PromptTemplate(
    template="""
    You are a helpful assistant.
    Answer only from the provided context.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    {context}
    Question: {question}
    Answer:
    """,
    input_variables=['context','question']
    )
    
    parser=StrOutputParser()
    

    chain = RunnableParallel({
        "context": retriever | RunnableLambda(lambda x: format_docs(x)),
        "question": RunnablePassthrough()
    }) | prompt | model | parser

    return chain


def summary():
    prompt = PromptTemplate(
        template="""You are an expert summarization system. Your task is to generate a large, comprehensive and detailed summary of the provided content. The summary must be thorough yet well-structured, retaining all crucial information, context, nuances, and supporting details.
        context:
        {context}

        Summary:""",
                input_variables=["context"]
            )

   

    parser = StrOutputParser()
    return prompt | model | parser



#path=r"D:\Proposal.pdf"
#path=r"D:\LangChain\text.txt"
#path=r"https://www.geeksforgeeks.org/machine-learning/introduction-machine-learning/"
#docs=process_file(path)
#docs=[Document(page_content=doc) for doc in documents]
# chain=qna(docs)
# question="What is Machine Learning?"
# answer=chain.invoke(question)
# print("Question:", question)
# print("Answer:", answer)


# summary_chain = summary()
# full_text = format_docs(docs)
# summary = summary_chain.invoke({"context": full_text})
# print("Summary:")
# print(summary)