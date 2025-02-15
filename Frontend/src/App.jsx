import React, { useState } from "react";
import HeartBackground from "./components/HeartBackground";
import ChatInput from "./components/ChatInput";
import ChatDisplay from "./components/ChatDisplay";
import "./components/background/background.css"; // Ensure styles are applied

const App = () => {
  const [messages, setMessages] = useState([]);

  const handleNewMessage = (msg) => {
    setMessages([...messages, msg]);
  };

  const handleClearMessages = () => {
    setMessages([]);
  };

  return (
    <div className="container">
      <HeartBackground />
      <ChatInput onMessageSubmit={handleNewMessage} onClearMessages={handleClearMessages} />
      <ChatDisplay messages={messages} />
    </div>
  );
};

export default App;