import eel
import logging
import constants
from db import message, chat
from llm import dispatch


logger = logging.getLogger(__name__)

# Functions defined in the front end that can be called from the backend

def js_update_current_message(message):
    eel.jsUpdateCurrentMessage(message)   


# Functions defined in the backend that can be called from the frontend

@eel.expose
def py_send_message(message_content, chat_id):
    logger.info(f"executing send_message function with {message_content}")

    current_chat = chat.get(chat_id)    

    message.create(constants.USER_ROLE, message_content, current_chat.id)
    saved_messages = message.list_by_chat(current_chat.id)

    response_message = ""
    try:
        stream = dispatch.send_message(saved_messages)
        for chunk in stream:
            content = chunk['message']['content']

            # update the frontend with the llm response in chunks
            js_update_current_message(content)

            # build the full response to save in the database
            response_message += content
    except Exception as error:
        # Without this the exception dies inside eel, the UI sits on an empty
        # "assistant:" line forever, and nothing says why. Show the failure in
        # the chat and skip saving a (partial or empty) assistant message.
        logger.exception("LLM request failed for chat %s", current_chat.id)
        js_update_current_message(f"[error] {error}")
        return

    message.create(constants.ASSISTANT_ROLE, response_message, current_chat.id)

@eel.expose
def py_delete_chat(chat_id):
    message.delete_by_chat(chat_id)
    chat.delete(chat_id)

@eel.expose
def py_create_chat(chat_name):
    return chat.create(chat_name).toFrontEnd()

@eel.expose
def py_get_chats():
    return [chatitem.toFrontEnd() for chatitem in chat.list()]
    
@eel.expose
def py_get_messages_by_chat(chat_id):
    return [messageitem.toFrontEnd() for messageitem in message.list_by_chat(chat_id)]


