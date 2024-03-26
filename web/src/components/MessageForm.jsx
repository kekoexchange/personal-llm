import { useState } from "react";

function MessageForm({ onSubmitForm }) {

  const [messageValue, setMessageValue] = useState("");

  const  handleChange = (event) => {
    setMessageValue(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    onSubmitForm(messageValue);
    setMessageValue("");
  }

  return (
    <>
      <h2>Message</h2>

      <form onSubmit={handleSubmit}>
        <fieldset>
          <label htmlFor="messageField">Message</label>
          <textarea placeholder="Hi Personal LLM …" onChange={handleChange} id="messageField" value={messageValue}></textarea>
          <div className="float-right">
            <input className="button-primary" type="submit" value="Send" />
          </div>
        </fieldset>
      </form>
    </>
  );
}

export default MessageForm;
