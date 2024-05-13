import eel
import logging
import db
import llm
import constants

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
  
@eel.expose
def py_main__send_chat(chat):
    logger.info(f"executing send_chat function with {chat}")

    db.insert_message("user", chat) 
    saved_messages = db.get_messages() 
    stream = llm.send_chat(saved_messages)

    response = ""
    for chunk in stream:
        # update the frontend with the llm reponse in chunks
        eel.js_app__updateCurrentChat(chunk['message']['content']) 

        # build the full response to save in the database
        response += chunk['message']['content']
    
    db.insert_message("assistant", response)

@eel.expose
def py_main__clear_chats():
    db.delete_messages()

def main():
    db.setup()
    eel.init(constants.FRONTEND_FOLDER)
    eel.start(constants.FRONTEND_INDEX_PAGE)

if __name__ == "__main__":
    main()