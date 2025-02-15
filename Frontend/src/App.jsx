import React, { useState } from "react";
import { v4 as uuidv4 } from "uuid";
import HeartBackground from "./components/HeartBackground";
import ChatInput from "./components/ChatInput";
import ChatDisplay from "./components/ChatDisplay";
import StatsPopup from "./components/StatsPopup";
import "./components/background/background.css";

const App = () => {
  const [messages, setMessages] = useState([]);
  const [stats, setStats] = useState(null);
  const sessionId = useState(uuidv4())[0];

  const handleNewMessage = (msg) => {
    setMessages((prevMessages) => [...prevMessages, msg]); // Append messages
  };

  const handleClearMessages = () => {
    setMessages([]);
  };

  const handleShowStats = (statsData) => {
    setStats(statsData); // Show stats popup
  };

  const handleCloseStats = () => {
    setStats(null); // Hide stats popup
  };

  return (
    <div className="container">
      <HeartBackground />
      <ChatDisplay messages={messages} />
      <ChatInput
        onMessageSubmit={handleNewMessage}
        onClearMessages={handleClearMessages}
        onShowStats={handleShowStats}
        sessionId={sessionId}
      />
      {stats && <StatsPopup stats={stats} onClose={handleCloseStats} />}
    </div>
  );
};

export default App;