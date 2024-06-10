import { useState, useEffect } from "react";

import MessageForm from "./components/MessageForm";
import MessageArea from "./components/MessageArea";
import ChatList from "./components/ChatList";
import * as Constants from "./utils/constants";

function App() {
  const [messageHistory, setMessageHistory] = useState([]);
  const [currentMessage, setCurrentMessage] = useState("");
  const [currentChatID, setCurrentChatID] = useState(Constants.NEW_CHAT_ID);
  const [allChats, setAllChats] = useState([]);

  useEffect(() => {
    eel.py_main__get_chats()((result) => {
      setAllChats(result);
      onChatNew();
    })
  }, []);

  const onChatNew = () => { 
    setMessageHistory([])
    setCurrentMessage("")
    setCurrentChatID(Constants.NEW_CHAT_ID)
  }

  const onChatSelect = (chatID) => {
    eel.py_main__get_messages_by_chat(chatID)((result) => {
      setMessageHistory(result.map((message) => `${message.role}: ${message.content}`));
      setCurrentMessage("")
    });
    setCurrentChatID(chatID);
  };

  const onSubmitForm = (textValue) => {
    if (currentMessage === "") {
      setMessageHistory([...messageHistory, `${Constants.USER_ROLE_NAME}: ${textValue}`]);
    } else {
      setMessageHistory([...messageHistory, currentMessage, `\n${Constants.USER_ROLE_NAME}: ${textValue}`]);
    }
    setCurrentMessage(`${Constants.ASSISTANT_ROLE_NAME}: `);

    if (currentChatID === Constants.NEW_CHAT_ID) {
      eel.py_main__create_chat(textValue.slice(0, Constants.NEW_CHAT_NAME_NUM_CHARS))((newChat) => {
        setAllChats([...allChats, newChat]);
        setCurrentChatID(newChat.id);
        eel.py_main__send_message(textValue, newChat.id)();
      });
    } else {
      eel.py_main__send_message(textValue, currentChatID)();
    }
    
  };

  const onChatDelete = () => {
    setAllChats((prevState) => prevState.filter((chat) => chat.id !== currentChatID));
    eel.py_main__delete_chat(currentChatID)(() => {
      onChatNew();
    });
  }

  eel.expose(js_app__updateCurrentMessage);
  function js_app__updateCurrentMessage(chunk) {
    setCurrentMessage((prevState) => prevState + chunk);
  }

  return (
    <div className="mg-container">
      <div className="mg-row">

        <div className="mg-col mg-x3">
          <div className="mg-row grid-cel chat-list">
            <ChatList allChats={allChats} currentChatID={currentChatID} onChatSelect={onChatSelect} />
          </div>
        </div>

        <div className="mg-col mg-x9">
          <div className="mg-row grid-cel message-area">
            <MessageArea messageHistory={messageHistory} currentMessage={currentMessage} />
          </div>
        </div>
      </div>
      <div className="mg-row message-form">
        <MessageForm onSubmitForm={onSubmitForm} onDeleteChat={onChatDelete} onNewChat={onChatNew} />
      </div>
    </div>
  );
}

export default App;

