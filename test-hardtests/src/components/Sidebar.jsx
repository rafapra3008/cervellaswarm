import React, { useState } from 'react';

const Sidebar = () => {
  const [notificationCount] = useState(3);

  return (
    <aside className="sidebar">
      <h3>Menu</h3>
      <ul>
        <li style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          Dashboard
          {notificationCount > 0 && (
            <span
              className="notification-badge"
              style={{
                backgroundColor: '#e74c3c',
                color: 'white',
                borderRadius: '50%',
                width: '24px',
                height: '24px',
                display: 'inline-flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '12px',
                fontWeight: 'bold'
              }}
            >
              {notificationCount}
            </span>
          )}
        </li>
        <li>Profilo</li>
        <li>Impostazioni</li>
      </ul>
    </aside>
  );
};

export default Sidebar;
