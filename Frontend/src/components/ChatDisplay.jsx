import React from "react";
import anime from "./background/anime";

const ChatDisplay = ({ messages }) => {
  return (
    <div id="displayContainer">
      {messages.map((msg, index) => (
        <div
          key={index}
          className={msg.sender === "User" ? "user-container" : "bot-container"}
        >
          <div
            className={`message-box ${msg.sender === "User" ? "user-message" : "bot-message"}`}
            ref={(el) => {
              if (el) {
                anime({
                  targets: el,
                  opacity: [0, 1],
                  translateY: [20, 0],
                  duration: 500,
                  easing: "easeOutQuad",
                });
              }
            }}
          >
            <span className="message-content">{msg.text}</span>
          </div>
        </div>
      ))}
    </div>
  );
};

export default ChatDisplay;
