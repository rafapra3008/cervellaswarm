import React from 'react';

interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary';
}

const Button: React.FC<ButtonProps> = ({
  label,
  onClick,
  variant = 'primary'
}) => {
  const baseStyles = {
    padding: '10px 20px',
    borderRadius: '8px',
    border: 'none',
    cursor: 'pointer',
    fontWeight: 600,
    fontSize: '14px',
    transition: 'all 0.2s ease',
  };

  const variantStyles = {
    primary: {
      backgroundColor: '#3b82f6',
      color: '#ffffff',
    },
    secondary: {
      backgroundColor: '#e5e7eb',
      color: '#374151',
    },
  };

  const combinedStyles = {
    ...baseStyles,
    ...variantStyles[variant],
  };

  return (
    <button
      style={combinedStyles}
      onClick={onClick}
    >
      {label}
    </button>
  );
};

export default Button;
