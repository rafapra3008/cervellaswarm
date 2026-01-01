import React from 'react';

// Funzione logout gia definita
const logout = () => {
  console.log('Logout clicked');
  // logica di logout
};

const Header = () => {
  return (
    <header className="header">
      <div className="logo">CervellaSwarm</div>
      <nav className="nav">
        <a href="/home">Home</a>
        <a href="/dashboard">Dashboard</a>
        <a href="/settings">Settings</a>
      </nav>
      <button
        className="logout-btn"
        onClick={logout}
        style={{
          backgroundColor: '#dc3545',
          color: 'white',
          border: 'none',
          borderRadius: '6px',
          padding: '8px 16px',
          cursor: 'pointer',
          fontSize: '14px',
          fontWeight: '500',
          transition: 'background-color 0.2s ease',
          marginLeft: 'auto'
        }}
        onMouseOver={(e) => e.target.style.backgroundColor = '#c82333'}
        onMouseOut={(e) => e.target.style.backgroundColor = '#dc3545'}
      >
        Logout
      </button>
    </header>
  );
};

export default Header;
