import React, { useState } from "react";
import { v4 as uuidv4 } from "uuid"; // Generate unique session IDs
import HeartBackground from "./components/HeartBackground";
import ChatInput from "./components/ChatInput";
import ChatDisplay from "./components/ChatDisplay";
import "./components/background/background.css";

const App = () => {
  const [messages, setMessages] = useState([]);
  const sessionId = useState(uuidv4())[0]; // Persistent session ID

  const handleNewMessage = (msg) => {
    setMessages([...messages, msg]);
  };

  return (
    <div className="container">
      <HeartBackground />
      <ChatDisplay messages={messages} />
      <ChatInput onMessageSubmit={handleNewMessage} sessionId={sessionId} />
    </div>
  );
};

export default App;