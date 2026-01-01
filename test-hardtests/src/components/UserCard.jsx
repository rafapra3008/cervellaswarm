import React from 'react';

const UserCard = ({ user }) => {
  return (
    <div className="user-card">
      <img src={user.avatar} alt={user.name} />
      <h3>{user.name}</h3>
      <p>{user.email}</p>
      {/* TODO: Mostrare badge Admin se utente e admin */}
    </div>
  );
};

export default UserCard;
