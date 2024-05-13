import React, { useEffect, useRef } from "react";

function MessageArea({ chatHistory, currentChat }) {
    const historyAreaRef = useRef(null);

    useEffect(() => {
      historyAreaRef.current.scrollTop = historyAreaRef.current.scrollHeight;
    }, [chatHistory, currentChat]);

    return (
      <div className="mg-col mg-x12">
        <pre>
          <code ref={historyAreaRef}>
            {chatHistory.map((chat) => chat + "\n")}
            {currentChat && currentChat + "\n"}
          </code>
        </pre>
      </div>
    );
}
export default MessageArea;