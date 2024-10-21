import boto3
import streamlit as st
import os
import uuid
import time

AWS_REGION = "us-west-2"

# S3 Client
s3_client = boto3.client("s3", region_name=AWS_REGION)
BUCKET_NAME = os.getenv("BUCKET_NAME")

# Bedrock
from langchain_aws import BedrockEmbeddings

# Text Splitter
from langchain.text_splitter import RecursiveCharacterTextSplitter

# PDF Loader
from langchain_community.document_loaders import PyPDFLoader

# FAISS
from langchain_community.vectorstores import FAISS

bedrock_client = boto3.client(service_name="bedrock-runtime", region_name=AWS_REGION)
bedrock_embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1", client=bedrock_client)

def get_unique_id():
    return str(uuid.uuid4())

# Split the pages / text into chunks
def split_text(pages, chunk_size, chunk_overlap):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = text_splitter.split_documents(pages)
    return docs

# Create Vector Store with detailed error logging
def create_vector_store(request_id, documents):
    if documents is None or len(documents) == 0:
        raise ValueError("No documents were passed for embedding.")

    st.write("Documents to be embedded (first 2 docs):")
    st.write(documents[:2])  # Print first 2 documents for inspection

    document_texts = [doc.page_content for doc in documents if doc.page_content.strip()]
    if not document_texts:
        raise ValueError("All documents are empty or contain invalid text.")

    st.write("Sending the following text for embedding (first 2 texts):")
    st.write(document_texts[:2])  # Log first 2 texts being sent for embeddings

    # Test with a simple text to isolate issues
    test_text = ["This is a simple test text to verify if embeddings work."]
    
    try:
        embeddings = bedrock_embeddings.embed_documents(test_text)
        st.write("Test Embedding Result:")
        st.write(embeddings)
    except Exception as e:
        st.write(f"Error while generating embeddings for test text: {e}")
        raise

    if embeddings is None or len(embeddings) == 0:
        raise ValueError("Failed to generate embeddings or received empty embeddings.")

    # Validate if embeddings are valid
    if embeddings[0] is None:
        raise ValueError("Error: Embeddings[0] is None, Bedrock might have returned invalid data.")

    # Proceed to FAISS vector store creation
    vectorstore_faiss = FAISS.from_documents(documents, bedrock_embeddings)

    file_name = f"{request_id}.bin"
    folder_path = "/tmp/"
    vectorstore_faiss.save_local(index_name=file_name, folder_path=folder_path)

    # Upload to S3
    s3_client.upload_file(Filename=folder_path + "/" + file_name + ".faiss", Bucket=BUCKET_NAME, Key="my_faiss.faiss")
    s3_client.upload_file(Filename=folder_path + "/" + file_name + ".pkl", Bucket=BUCKET_NAME, Key="my_faiss.pkl")

    return True

# Main method
def main():
    st.write("This is Admin Site for Chat with PDF demo")
    uploaded_file = st.file_uploader("Choose a file", "pdf")
    
    if uploaded_file is not None:
        request_id = get_unique_id()
        st.write(f"Request Id: {request_id}")
        
        saved_file_name = f"{request_id}.pdf"
        with open(saved_file_name, mode="wb") as w:
            w.write(uploaded_file.getvalue())

        loader = PyPDFLoader(saved_file_name)
        pages = loader.load_and_split()

        if pages is None:
            st.write("Error: Failed to load PDF. Please check the file.")
            return

        st.write(f"Total Pages: {len(pages)}")

        # Split Text
        splitted_docs = split_text(pages, 1000, 200)
        st.write(f"Splitted Docs length: {len(splitted_docs)}")
        st.write("===================")
        st.write(splitted_docs[0])
        st.write("===================")
        st.write(splitted_docs[1])

        st.write("Creating the Vector Store")
        
        try:
            result = create_vector_store(request_id, splitted_docs)
        except ValueError as e:
            st.write(f"Error while creating vector store: {e}")
            return

        if result:
            st.write("Hurray!! PDF processed successfully")
        else:
            st.write("Error!! Please check logs.")

if __name__ == "__main__":
    main()
