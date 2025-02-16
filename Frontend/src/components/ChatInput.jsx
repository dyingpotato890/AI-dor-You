import React, { useState } from "react";
import { ArrowUp } from "lucide-react"; // Importing the arrow icon

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

        const textResponse = await response.text();
        let data;

        try {
          data = JSON.parse(textResponse);
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
      <button
        id="submitBtn"
        onClick={handleSubmit}
        disabled={loading}
        style={{
          backgroundColor: "##ff007f",
          border: "none",
          width: "40px",
          height: "40px",
          borderRadius: "50%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          cursor: loading ? "not-allowed" : "pointer",
          opacity: loading ? 0.6 : 1,
          transition: "background 0.3s ease",
          boxShadow: "0 2px 4px rgba(255, 0, 234, 0.2)",
        }}
      >
        <ArrowUp size={20} color="#ff007f" /> {/* Pink color */}
      </button>
    </div>
  );
};

export default ChatInput;
