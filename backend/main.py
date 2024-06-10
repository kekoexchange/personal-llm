import eel
import logging
import constants
from db import message, chat
from llm import dispatch
from db.utils import setup as db_setup

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

  
@eel.expose
def py_main__send_message(message_content, chat_id):
    logger.info(f"executing send_message function with {message_content}")

    current_chat = chat.get(chat_id)    

    message.create(constants.USER_ROLE, message_content, current_chat.id)
    saved_messages = message.list_by_chat(current_chat.id)
    stream = dispatch.send_message(saved_messages)

    response_message = ""
    for chunk in stream:
        # update the frontend with the llm reponse in chunks
        eel.js_app__updateCurrentMessage(chunk['message']['content']) 

        # build the full response to save in the database
        response_message += chunk['message']['content']
    
    message.create(constants.ASSISTANT_ROLE, response_message,  current_chat.id)

@eel.expose
def py_main__delete_chat(chat_id):
    message.delete_by_chat(chat_id)
    chat.delete(chat_id)

@eel.expose
def py_main__create_chat(chat_name):
    return chat.create(chat_name).toFrontEnd()

@eel.expose
def py_main__get_chats():
    return [chatitem.toFrontEnd() for chatitem in chat.list()]
    
@eel.expose
def py_main__get_messages_by_chat(chat_id):
    return [messageitem.toFrontEnd() for messageitem in message.list_by_chat(chat_id)]

def main():
    db_setup()

    eel.init(constants.FRONTEND_FOLDER)
    eel.start(constants.FRONTEND_INDEX_PAGE)

if __name__ == "__main__":
    main()