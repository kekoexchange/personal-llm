import { useState } from "react";

function MessageForm({ onSubmitForm, onClearForm }) {

  const [messageValue, setMessageValue] = useState("");

  const handleChange = (event) => {
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
    setMessageValue();
  }

  const handleEnterPress = (event) => {
    if(event.keyCode == 13 && event.shiftKey == false) {
      event.preventDefault();
      handleSubmit(event);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="mg-col mg-x12">
      <fieldset>
        <label htmlFor="messageField">Message</label>
        <div className="mg-row">
          <div className="mg-col mg-x12">
            <textarea placeholder="Ask the assistant, press Enter to send" onChange={handleChange} onKeyDown={handleEnterPress} id="messageField" value={messageValue} />
          </div>
        </div>
        <div className="mg-row">
          <div className="mg-col mg-x2">
            <button className="mg-bg-tertiary" style={{ border: 'none' }} onClick={handleClear}>Clear</button>
          </div>
          <div className="mg-col, mg-x8"></div>
          <div className="mg-col mg-x2">
            <button>Send</button>
          </div>
        </div>
      </fieldset>
    </form>
  );
}

export default MessageForm;
