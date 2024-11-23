from src.helper import load_embedding,load_repo,text_splitter,repo_ingestion
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
import os


load_dotenv()
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
os.environ['GEMINI_API_KEY'] = GEMINI_API_KEY

documents = load_repo('repo/')

text_chunks = text_splitter(documents)

embeddings = load_embedding()

vectordb = Chroma.from_documents(text_chunks,embedding=embeddings,persist_directory= "./db")
