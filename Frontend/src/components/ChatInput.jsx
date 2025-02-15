import React, { useState } from "react";

const ChatInput = ({ onMessageSubmit, onClearMessages }) => {
  const [text, setText] = useState("");

  const handleSubmit = () => {
    if (text.trim()) {
      onMessageSubmit(text);
      setText("");
    }
  };

  return (
    <div className="input-container">
      <button id="endChatBtn" onClick={onClearMessages}>End</button>
      <input
        type="text"
        id="textInput"
        placeholder="Type your text here..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <button id="submitBtn" onClick={handleSubmit}>
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="12" cy="12" r="11" stroke="pink" strokeWidth="2" fill="white" />
          <path d="M12 7L12 17M12 7L8 11M12 7L16 11" stroke="pink" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </button>
    </div>
  );
};

export default ChatInput;