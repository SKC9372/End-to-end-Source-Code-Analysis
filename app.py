import os 
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationSummaryBufferMemory
from langchain.chains import ConversationalRetrievalChain 

from flask import Flask,render_template,jsonify,request
from src.helper import load_embedding,load_repo,text_splitter,repo_ingestion

app = Flask(__name__)

load_dotenv()
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
os.environ['GEMINI_API_KEY'] = GEMINI_API_KEY

embeddings = load_embedding()

persist_directory = 'db'

vectordb = Chroma(persist_directory=persist_directory,embedding_function=embeddings)

llm = ChatGoogleGenerativeAI(model='gemini-1.5-pro',max_tokens=500,temperature=0.3)
memory = ConversationSummaryBufferMemory(llm=llm,memory_key="chat_history",return_messages=True)

qa = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vectordb.as_retriever(search_type="mmr", search_kwargs={"k": 3}),
    memory=memory  # Attach memory to the chain
)

@app.route('/',methods = ["GET","POST"])
def index():
    return render_template("index.html")


@app.route('/chatbot',methods = ["GET","POST"])
def gitrepo():

    if request.method == "POST":
        user_input = request.form['question']
        repo_ingestion(user_input)

        os.system("python store_index.py")

    return jsonify({"response": str(user_input)})

@app.route("/get",methods = ["GET","POST"])
def chat():
    msg = request.form['msg']
    input = msg
    print(input)

    if input == 'clear':
        os.system("rm -rf repo")
        return 'Repository cleared from database'

    result = qa.invoke(input)
    return result['answer']

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080,debug=True)