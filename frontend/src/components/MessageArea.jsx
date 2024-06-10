import React, { useEffect, useRef } from "react";

function MessageArea({ messageHistory, currentMessage }) {
    const historyAreaRef = useRef(null);

    useEffect(() => {
      historyAreaRef.current.scrollTop = historyAreaRef.current.scrollHeight;
    }, [messageHistory, currentMessage]);

    return (
      <div className="mg-col mg-x12">
        <pre>
          <code ref={historyAreaRef}>
            {messageHistory && messageHistory.length > 0 && messageHistory.map((message) => message + "\n====================\n")}
            {currentMessage}
          </code>
        </pre>
      </div>
    );
}
export default MessageArea;