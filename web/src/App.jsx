import { useState } from "react";

import MessageForm from "./components/MessageForm";

function App() {

  const [chatHistory, setChatHistory] = useState([]);

  const onSubmitForm = (messageValue) => {
    eel.sendMessage(messageValue)(function(newMessage) {
      setChatHistory([...chatHistory, newMessage]);
    })
  };

  return (
    <>
      <h1>Welcome to Personal LLM!</h1>

      <h2>Chat History</h2>

      <ul>
        {chatHistory.map((chat) => <li>{chat}</li>)}
      </ul>
      
      <MessageForm onSubmitForm={onSubmitForm} />
    </>
  );
}

export default App;
