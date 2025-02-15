import React, { useState } from "react";

const ChatInput = ({ onMessageSubmit, onClearMessages, sessionId }) => {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (text.trim()) {
      const userMessage = text;
      onMessageSubmit({ sender: "User", text: userMessage });
      setText("");
      setLoading(true);

      try {
        const response = await fetch("http://127.0.0.1:5000/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ session_id: sessionId, message: userMessage }),
        });

        const data = await response.json();
        onMessageSubmit({ sender: "AI", text: data.response });
      } catch (error) {
        console.error("Error sending message:", error);
        onMessageSubmit({ sender: "AI", text: "Failed to get a response." });
      } finally {
        setLoading(false);
      }
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
        disabled={loading}
      />
      <button id="submitBtn" onClick={handleSubmit} disabled={loading}>
        {loading ? "..." : "Send"}
      </button>
    </div>
  );
};

export default ChatInput;