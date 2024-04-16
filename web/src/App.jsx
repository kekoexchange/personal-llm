import { useState } from "react";

import MessageForm from "./components/MessageForm";

function App() {

  const [chatHistory, setChatHistory] = useState([]);
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
    <div className="container">

      <div className="row">
        <h1 class="column">Welcome to Personal LLM!</h1>
      </div>

      <div className="row history">
        <pre class="column">
          {chatHistory.map((chat) => chat + "\n")}
          {currentChat && (currentChat + "\n") }
        </pre>
      </div>

      <MessageForm onSubmitForm={onSubmitForm} onClearForm={onClearForm} className="row" />
    </div>
  );
}

export default App;
