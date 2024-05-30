import eel
import logging
import constants
from db import message
from llm import dispatch
from db.utils import setup as db_setup, get_default_chat as db_get_default_chat

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# TODO: Temporary chat object until the frontend is implemented
default_chat = None
  
@eel.expose
def py_main__send_message(message_content):
    logger.info(f"executing send_message function with {message_content}")

    message.create(constants.USER_ROLE, message_content, default_chat)
    saved_messages = message.list()
    stream = dispatch.send_message(saved_messages)

    response_message = ""
    for chunk in stream:
        # update the frontend with the llm reponse in chunks
        eel.js_app__updateCurrentChat(chunk['message']['content']) 

        # build the full response to save in the database
        response_message += chunk['message']['content']
    
    message.create(constants.ASSISTANT_ROLE, response_message, default_chat)

@eel.expose
def py_main__clear_messages():
    message.delete_by_chat(default_chat)

def main():
    db_setup()

    # TODO: Temporary code to return the default chat object until the frontend is implemented
    global default_chat
    default_chat = db_get_default_chat()

    eel.init(constants.FRONTEND_FOLDER)
    eel.start(constants.FRONTEND_INDEX_PAGE)

if __name__ == "__main__":
    main()