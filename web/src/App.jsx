import { useState } from "react";

import MessageForm from "./components/MessageForm";

function App() {

  const [chatHistory, setChatHistory] = useState([]);
  const [currentChat, setCurrentChat] = useState("");

  const USER_ROLE = "User";
  const ASSISTANT_ROLE = "Assistant";
  const GET_CHAT_POLLING_FREQUENCY_IN_MS = 50;

  const onSubmitForm = (textValue) => {
    if (currentChat === "") {
      setChatHistory([...chatHistory, `${USER_ROLE}: ${textValue}`]);
    } else {
      setChatHistory([...chatHistory, currentChat, `\n${USER_ROLE}: ${textValue}`]);
    }

    setCurrentChat(`${ASSISTANT_ROLE}: `);

    eel.send_chat(textValue)(() => {
      let chatGPTInterval = setInterval(() => {
        eel.get_chat_response_in_chunks()((chunk) => {
          if (chunk === null) {
            clearInterval(chatGPTInterval);
          } else {
            setCurrentChat((prevState) => prevState + chunk);
          }
        });
      }, GET_CHAT_POLLING_FREQUENCY_IN_MS);
    });

  };

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

      <MessageForm onSubmitForm={onSubmitForm} className="row" />
    </div>
  );
}

export default App;
