import React, { useState, useEffect } from 'react';
import './Tooltip.css';

const Tooltip: React.FC = () => {
  const [visibility, setVisibility] = useState<'hidden' | 'visible'>('hidden');

  useEffect(() => {
    const showTooltip = () => setVisibility('visible');
    const hideTooltip = () => setVisibility('hidden');

    const tooltip = document.getElementById('myTooltip');
    if (tooltip) {
      tooltip.addEventListener('mouseover', showTooltip);
      tooltip.addEventListener('mouseout', hideTooltip);
    }

    // cleanup function
    return () => {
      if (tooltip) {
        tooltip.removeEventListener('mouseover', showTooltip);
        tooltip.removeEventListener('mouseout', hideTooltip);
      }
    };
  }, []); // empty dependency array means this effect runs once on mount and cleanup on unmount

  return (
    <div id="myTooltip" className="tooltip" style={{ cursor: 'pointer' }}>
      Hover over me
      <span className="tooltiptext" style={{ visibility: visibility, transition: 'opacity 0.3s' }}>
        Tooltip text
      </span>
    </div>
  );
};

export default Tooltip;
