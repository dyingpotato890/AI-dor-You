import React from "react";

const StatsPopup = ({ stats, onClose }) => {
  if (!stats) return null; // Don't show if no stats available

  return (
    <div className="popup-overlay">
      <div className="popup-content">
        <h2>Chat Statistics</h2>
        <pre>{stats}</pre>
        <button onClick={onClose}>Close</button>
      </div>
    </div>
  );
};

export default StatsPopup;