import React, { useMemo } from "react";

const StatsPopup = ({ stats, onClose }) => {
  if (!stats) return null; // Don't show if no stats available

  const parsedStats = useMemo(() => {
    try {
      return JSON.parse(stats);
    } catch (error) {
      console.error("Error parsing stats JSON:", stats);
      return { error: "Invalid stats format received." };
    }
  }, [stats]);

  return (
    <div style={styles.overlay}>
      <div style={styles.popup}>
        <h2 style={styles.heading}>Chat Statistics</h2>
        {parsedStats.error ? (
          <p style={styles.text}>{parsedStats.error}</p>
        ) : (
          <div>
            <p style={styles.text}><strong>Flirt Score:</strong> {parsedStats["Flirt Score"] || "N/A"}</p>
            <p style={styles.text}><strong>Chat Analysis:</strong> {parsedStats["Chat Analysis"] || "N/A"}</p>
            <p style={styles.text}><strong>Stronger Areas:</strong> {parsedStats["Stronger Areas"] || "N/A"}</p>
            <p style={styles.text}><strong>Flaws & Areas for Improvement:</strong> {parsedStats["Flaws & Areas for Improvement"] || "N/A"}</p>
            <p style={styles.text}><strong>Tips for Next Date:</strong> {parsedStats["Tips for Next Date"] || "N/A"}</p>
          </div>
        )}
        <button style={styles.button} onClick={onClose}>Close</button>
      </div>
    </div>
  );
};

// Styles (inline)
const styles = {
  overlay: {
    position: "fixed",
    top: 0,
    left: 0,
    width: "100%",
    height: "100%",
    background: "rgba(0, 0, 0, 0.5)",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    zIndex: 1000,
  },
  popup: {
    background: "#ffe0f0",
    borderRadius: "12px",
    padding: "20px",
    width: "350px",
    textAlign: "center",
    fontFamily: "Arial, sans-serif",
    color: "#d63384",
  },
  text: {
    fontSize: "16px",
    margin: "8px 0",
  },
  button: {
    background: "#ff4d94",
    color: "white",
    padding: "10px 20px",
    borderRadius: "8px",
  },
};

export default StatsPopup;
