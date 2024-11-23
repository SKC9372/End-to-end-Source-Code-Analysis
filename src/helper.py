from git import Repo
from langchain.text_splitter import Language
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers.language.language_parser import LanguageParser
from langchain.text_splitter import RecursiveCharacterTextSplitter

import os 

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationalRetrievalChain 

# Clone any github repositories

def repo_ingestion(repo_url):
    os.makedirs("repo",exist_ok=True)
    repo_path = "repo/"
    repo = Repo.clone_from(repo_url,to_path=repo_path)



# Loading repositories in document
def load_repo(repo_path):
    loader = GenericLoader.from_filesystem(repo_path,
                                         glob="**/*",
                                         suffixes=[".py"],
                                         parser=LanguageParser(Language.PYTHON,parser_threshold=500))
    documents =  loader.load()
    return documents


# Splitting the documents
def text_splitter(documents):
    documents_splitter = RecursiveCharacterTextSplitter.from_language(language=Language.PYTHON,
                                                                      chunk_size = 500,
                                                                      chunk_overlap = 20)
    
    text_chunks = documents_splitter.split_documents(documents)

    return text_chunks


# loading Embedding model

def load_embedding():
    embeddings = GoogleGenerativeAIEmbeddings(model='models/embedding-001')
    return embeddings
