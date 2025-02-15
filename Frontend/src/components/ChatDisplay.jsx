import React from "react";
import anime from "./background/anime";

const ChatDisplay = ({ messages }) => {
  return (
    <div id="displayContainer">
      {messages.map((msg, index) => (
        <p
          key={index}
          style={{ opacity: 0 }}
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
          {msg}
        </p>
      ))}
    </div>
  );
};

export default ChatDisplay;