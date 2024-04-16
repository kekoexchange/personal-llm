import { useState } from "react";

function MessageForm({ onSubmitForm, onClearForm }) {

  const [messageValue, setMessageValue] = useState("");

  const  handleChange = (event) => {
    setMessageValue(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    onSubmitForm(messageValue);
    setMessageValue("");
  }

  const handleClear = (event) => {
    event.preventDefault();
    onClearForm();
    setMessageValue("");
  }

  return (
    <form onSubmit={handleSubmit}>
      <fieldset>
        <label htmlFor="messageField">Message</label>
        <textarea placeholder="Ask the assistant" onChange={handleChange} id="messageField" value={messageValue} />
        <div className="float-right">
          <input className="button-primary" type="button" value="Clear" onClick={handleClear} />
          <input className="button-primary" type="submit" value="Send" />
        </div>
      </fieldset>
    </form>
  );
}

export default MessageForm;
