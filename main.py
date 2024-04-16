import eel
import ollama
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

eel.init("web")   
LLM_MODEL = "tinyllama:chat"
system_prompt = """
    You are a friendly chatbot. 
    You are helpful, kind, honest, and good at writing. 
    You do not repeat yourself. 
    You keep it short unless instructed otherwise.
    """
  
@eel.expose     
def py_main__send_chat(chat): 
    logger.info(f"executing send_chat function with {chat}")

    stream = ollama.chat(
        model=LLM_MODEL,
        messages=[
            { 
                'role': 'system', 
                'content': system_prompt
            },
            {
                'role': 'user',
                'content': chat
            }
        ],
        stream=True,
    )
    for chunk in stream:
        eel.js_app__updateCurrentChat(chunk['message']['content'])
      
eel.start("index.html")