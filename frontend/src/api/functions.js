

// backend functions to be called from the frontend
export const pySendMessage = (message, chatID, callback=()=>{}) => {
    eel.py_send_message(message, chatID)(callback);
};

export const pyDeleteChat = (chatID, callback=()=>{}) => {
    eel.py_delete_chat(chatID)(callback);
};

export const pyGetChats = (callback=()=>{}) => {
    eel.py_get_chats()(callback);
};

export const pyCreateChat = (name, callback=()=>{}) => {
    eel.py_create_chat(name)(callback);
};

export const pyGetMessagesByChat = (chatID, callback=()=>{}) => {
    eel.py_get_messages_by_chat(chatID)(callback);
};


// In case an eel function that is exposed to the backend
// requires dynamically created resources, use 
// eelResources to pass those resources here
export const eelResources = {}

// frontend functions to be called from the backend

eel.expose(jsUpdateCurrentMessage);
function jsUpdateCurrentMessage(chunk) {
    eelResources.jsUpdateCurrentMessage.setCurrentMessage((prevState) => prevState + chunk);
}
