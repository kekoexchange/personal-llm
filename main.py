import eel
import ollama
import logging
import data_layer

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

eel.init("web")   
LLM_MODEL = "llama3:latest"
system_prompt = """
    You are a friendly chatbot. 
    You are helpful, kind, honest, and good at writing. 
    You do not repeat yourself. 
    You keep it short unless instructed otherwise.
    """

data_layer.setup()
  
@eel.expose
def py_main__send_chat(chat):
    logger.info(f"executing send_chat function with {chat}")

    data_layer.insert_message("user", chat)  # Save the message using data_layer function
    saved_messages = data_layer.retrieve_all_messages()  # Get all messages from data_layer

    all_messages = [{
                'role': 'system',
                'content': system_prompt
                }]
    all_messages.extend([
        {
            'role': role,
            'content': content
        }
        for role, content in saved_messages
    ])

    stream = ollama.chat(
        model=LLM_MODEL,
        messages=all_messages,
        stream=True,
    )

    response = ""
    for chunk in stream:
        eel.js_app__updateCurrentChat(chunk['message']['content'])
        response += chunk['message']['content']
    
    data_layer.insert_message("assistant", response)


@eel.expose
def py_main__clear_chats():
    data_layer.clear_messages()

eel.start("index.html")