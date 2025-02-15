import React, { useEffect, useRef } from "react";
import anime from "./background/anime"; // Using the anime.js library
import "./background/background.css"; // Import styles

const HeartBackground = () => {
  const containerRef = useRef(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    // Generate hearts
    for (let i = 0; i <= 100; i++) {
      const heart = document.createElement("div");
      heart.classList.add("heart");
      container.appendChild(heart);
    }

    function animateHearts() {
      anime({
        targets: ".heart",
        translateX: () => anime.random(-700, 700),
        translateY: () => anime.random(-500, 500),
        rotate: 45,
        scale: () => anime.random(1, 3),
        easing: "easeInOutBack",
        duration: 3000,
        delay: anime.stagger(10),
        complete: animateHearts,
      });
    }

    animateHearts();
  }, []);

  return <div ref={containerRef} className="container"></div>;
};

export default HeartBackground;