import { useState } from "react";

import MessageForm from "./components/MessageForm";

function App() {

  const [chatHistory, setChatHistory] = useState([
`******************************
Welcome to Personal LLM! Ask me anything! Enter in the form below
******************************`]);
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

      <header className="row header">
        <div className="column">
          <span>Personal LLM: Your local personal assistant</span>
        </div>
      </header>

      <div className="row history">
        <pre class="column">
          {chatHistory.map((chat) => chat + "\n")}
          {currentChat && (currentChat + "\n") }
        </pre>
      </div>
      
      <div className="row space-between">
        &nbsp;
      </div>

      <MessageForm onSubmitForm={onSubmitForm} onClearForm={onClearForm} className="row" />


      <footer className="row footer">
        <div className="column">
        </div>
        <div className="column">
          <em>Brought to you by the folks from <a href="https://kekoexchange.com" _target="_blank">Kekoexchange</a></em>
        </div>
        <div className="column">&nbsp;</div>
      </footer>
    </div>
  );
}

export default App;
