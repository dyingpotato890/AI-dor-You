import React, { useState } from "react";

const ChatInput = ({ onMessageSubmit, onClearMessages, onShowStats, sessionId }) => {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (text.trim()) {
      onMessageSubmit({ sender: "User", text });
      setText("");
      setLoading(true);

      try {
        const response = await fetch("https://ai-dor-you-2.onrender.com/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ session_id: sessionId, message: text }),
        });

        if (!response.ok) {
          throw new Error(`Server responded with ${response.status}`);
        }

        const textResponse = await response.text(); // Read as text first
        let data;

        try {
          data = JSON.parse(textResponse); // Attempt JSON parsing
        } catch (error) {
          console.error("Invalid JSON received:", textResponse);
          throw new Error("Invalid JSON format from API");
        }

        if (!data || typeof data.response !== "string") {
          throw new Error("Unexpected response format");
        }

        onMessageSubmit({ sender: "AI", text: data.response });
      } catch (error) {
        console.error("Error sending message:", error);
        onMessageSubmit({ sender: "AI", text: "Failed to get a valid response from the server." });
      } finally {
        setLoading(false);
      }
    }
  };

  const handleEndChat = async () => {
    setLoading(true);
    onClearMessages(); // Clear chat history before fetching stats

    try {
      const response = await fetch("https://ai-dor-you-2.onrender.com/stats", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId }),
      });

      if (!response.ok) {
        throw new Error(`Server responded with ${response.status}`);
      }

      const textResponse = await response.text();
      let data;

      try {
        data = JSON.parse(textResponse);
      } catch (error) {
        console.error("Invalid JSON received:", textResponse);
        throw new Error("Invalid JSON format from API");
      }

      if (typeof data.stats === "object") {
        onShowStats(JSON.stringify(data.stats, null, 2));
      } else {
        onShowStats('{"error": "Failed to generate statistics."}');
      }
    } catch (error) {
      console.error("Error fetching stats:", error);
      onShowStats('{"error": "Failed to generate statistics."}');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="input-container">
      <button id="endChatBtn" onClick={handleEndChat} disabled={loading}>
        {loading ? "Ending..." : "End"}
      </button>
      <input
        type="text"
        id="textInput"
        placeholder="Type your message..."
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
