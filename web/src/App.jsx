import { useState, useEffect, useRef } from "react";

import MessageForm from "./components/MessageForm";
import * as Constants from "./utils/constants";

function App() {

  const [chatHistory, setChatHistory] = useState([Constants.INTRO_MESSAGE]);
  const [currentChat, setCurrentChat] = useState("");
  const historyAreaRef = useRef(null);

  useEffect(() => {
    historyAreaRef.current.scrollTop = historyAreaRef.current.scrollHeight;
  }, [chatHistory, currentChat]);

  eel.expose(js_app__updateCurrentChat);
  function js_app__updateCurrentChat(chunk) {
    setCurrentChat((prevState) => prevState + chunk);
  }

  const onSubmitForm = (textValue) => {
    if (currentChat === "") {
      setChatHistory([...chatHistory, `${Constants.USER_ROLE_NAME}: ${textValue}`]);
    } else {
      setChatHistory([...chatHistory, currentChat, `\n${Constants.USER_ROLE_NAME}: ${textValue}`]);
    }

    setCurrentChat(`${Constants.ASSISTANT_ROLE_NAME}: `);

    eel.py_main__send_chat(textValue)();
  };

  const onClearForm = () => {
    setCurrentChat("");
    setChatHistory([Constants.INTRO_MESSAGE]);
    eel.py_main__clear_chats()();
  }

  return (
    <div className="mg-container">

      <div className="mg-row">

        <div className="mg-col mg-x12 history">
          <pre><code ref={historyAreaRef}>
            {chatHistory.map((chat) => chat + "\n")}
            {currentChat && (currentChat + "\n") }
          </code></pre>
        </div>
      </div>

      <MessageForm onSubmitForm={onSubmitForm} onClearForm={onClearForm} className="mg-row message" />
    </div>
  );
}

export default App;
