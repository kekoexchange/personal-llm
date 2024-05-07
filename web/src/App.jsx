import { useState } from "react";

import MessageForm from "./components/MessageForm";

function App() {

  const [chatHistory, setChatHistory] = useState([
`******************************
Welcome to Personal LLM! Ask me anything! Enter in the form below
******************************\n`]);
  const [currentChat, setCurrentChat] = useState("");

  const USER_ROLE = "User";
  const ASSISTANT_ROLE = "Assistant";

  eel.expose(js_app__updateCurrentChat);
  function js_app__updateCurrentChat(chunk) {
    setCurrentChat((prevState) => prevState + chunk);
  }

  const onSubmitForm = (textValue) => {
    if (currentChat === "") {
      setChatHistory([...chatHistory, `${USER_ROLE}: ${textValue}`]);
    } else {
      setChatHistory([...chatHistory, currentChat, `\n${USER_ROLE}: ${textValue}`]);
    }

    setCurrentChat(`${ASSISTANT_ROLE}: `);

    eel.py_main__send_chat(textValue)();
  };

  const onClearForm = () => {
    setCurrentChat("");
    setChatHistory([]);
    eel.py_main__clear_chats()();
  }

  return (
    <div className="mg-container">

      <div className="mg-row">

        <div className="mg-col mg-x12 history">
          <pre><code>
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
