import eel   

from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

eel.init("web")   

chat_buffer = []
LLM_MODEL = "tinyllama:chat"
  
@eel.expose     
def send_chat(chat): 
    print(f"executing send_chat function with {chat}")
    llm = ChatOllama(model=LLM_MODEL)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a friendly chatbot. You are helpful, kind, honest, and good at writing. You do not repeat yourself. You keep it short unless instructed otherwise."),
        ("human", "{chat}"),
    ])
    chain = prompt | llm | StrOutputParser()

    parameters = {"chat": chat}

    for chunk in chain.stream(parameters):
        chat_buffer.append(chunk)
        
@eel.expose   
def get_chat_response_in_chunks():

    chunk = None
    if chat_buffer:
        chunk = chat_buffer.pop(0)

    return chunk
      
eel.start("index.html")