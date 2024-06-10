import React from "react";

function ChatList({ allChats, currentChatID, onChatSelect }) {

    return (
        <div className="mg-col mg-x12">
            <ul>
            {allChats.map((chat) => (
            <li key={chat.id} onClick={() => onChatSelect(chat.id)} className={(chat.id == currentChatID) ? 'selected':''}>
                {chat.name}
            </li>
            ))}
        </ul>
    </div>
    );
}
export default ChatList;