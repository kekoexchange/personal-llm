import { useState } from "react";

import MessageForm from "./components/MessageForm";
import MessageArea from "./components/MessageArea";
import * as Constants from "./utils/constants";

function App() {
  const [chatHistory, setChatHistory] = useState([Constants.INTRO_MESSAGE]);
  const [currentChat, setCurrentChat] = useState("");

  const onSubmitForm = (textValue) => {
    if (currentChat === "") {
      setChatHistory([...chatHistory, `${Constants.USER_ROLE_NAME}: ${textValue}`]);
    } else {
      setChatHistory([...chatHistory, currentChat, `\n${Constants.USER_ROLE_NAME}: ${textValue}`]);
    }
    setCurrentChat(`${Constants.ASSISTANT_ROLE_NAME}: `);
    eel.py_main__send_message(textValue)();
  };

  const onClearForm = () => {
    setCurrentChat("");
    setChatHistory([Constants.INTRO_MESSAGE]);
    eel.py_main__clear_messages()();
  };

  eel.expose(js_app__updateCurrentChat);
  function js_app__updateCurrentChat(chunk) {
    setCurrentChat((prevState) => prevState + chunk);
  }

  return (
    <div className="mg-container">
      <div className="mg-row message-area">
        <MessageArea chatHistory={chatHistory} currentChat={currentChat} />
      </div>
      <div className="mg-row message-form">
        <MessageForm onSubmitForm={onSubmitForm} onClearForm={onClearForm} />
      </div>
    </div>
  );
}

export default App;

