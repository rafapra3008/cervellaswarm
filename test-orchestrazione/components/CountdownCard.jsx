// @version 1.0.0
// @date 2026-01-01
// CountdownCard - Componente per countdown a eventi specifici

import React, { useState, useEffect } from 'react';

const CountdownCard = ({ targetDate, eventName }) => {
  const [countdownData, setCountdownData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchCountdown();
  }, [targetDate, eventName]);

  const fetchCountdown = async () => {
    try {
      setLoading(true);
      const response = await fetch(`/api/countdown?target=${targetDate}&event=${encodeURIComponent(eventName)}`);
      const data = await response.json();

      if (data.status === 'success') {
        setCountdownData(data.data);
      } else {
        setError('Errore nel caricamento del countdown');
      }
    } catch (err) {
      setError('Impossibile connettersi al server');
      console.error('Errore fetch countdown:', err);
    } finally {
      setLoading(false);
    }
  };

  // Determina colore sfondo in base allo stato
  const getBackgroundStyle = () => {
    if (!countdownData) return {};

    if (countdownData.is_today) {
      // Oggi: blu celebrativo
      return {
        background: 'linear-gradient(135deg, #60A5FA 0%, #2563EB 100%)',
        color: '#FFFFFF'
      };
    } else if (countdownData.is_past) {
      // Passato: grigio
      return {
        background: 'linear-gradient(135deg, #9CA3AF 0%, #6B7280 100%)',
        color: '#F3F4F6'
      };
    } else if (countdownData.days_remaining <= 7) {
      // Prossimo (1-7 giorni): arancione
      return {
        background: 'linear-gradient(135deg, #FB923C 0%, #EA580C 100%)',
        color: '#FFFFFF'
      };
    } else {
      // Futuro (>7 giorni): verde
      return {
        background: 'linear-gradient(135deg, #34D399 0%, #10B981 100%)',
        color: '#064E3B'
      };
    }
  };

  const cardStyle = {
    ...getBackgroundStyle(),
    borderRadius: '16px',
    padding: '32px',
    maxWidth: '400px',
    margin: '0 auto',
    boxShadow: '0 8px 24px rgba(0, 0, 0, 0.15)',
    transition: 'transform 0.3s ease, box-shadow 0.3s ease',
    cursor: 'pointer',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
  };

  const eventNameStyle = {
    fontSize: '24px',
    fontWeight: '600',
    marginBottom: '16px',
    textAlign: 'center',
    letterSpacing: '-0.3px'
  };

  const daysRemainingStyle = {
    fontSize: '48px',
    fontWeight: '700',
    textAlign: 'center',
    marginBottom: '8px',
    letterSpacing: '-1px'
  };

  const targetDateStyle = {
    fontSize: '16px',
    fontWeight: '500',
    textAlign: 'center',
    opacity: '0.9'
  };

  const loadingStyle = {
    ...cardStyle,
    background: 'linear-gradient(135deg, #E5E7EB 0%, #D1D5DB 100%)',
    color: '#6B7280'
  };

  const errorStyle = {
    ...cardStyle,
    background: 'linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%)',
    color: '#991B1B'
  };

  // Stati loading ed errore
  if (loading) {
    return (
      <div style={loadingStyle}>
        <div style={daysRemainingStyle}>...</div>
        <div style={eventNameStyle}>Caricamento...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div style={errorStyle}>
        <div style={eventNameStyle}>Ops!</div>
        <div style={targetDateStyle}>{error}</div>
      </div>
    );
  }

  // Testo descrittivo in base allo stato
  const getStatusText = () => {
    if (countdownData.is_today) {
      return 'È oggi! 🎉';
    } else if (countdownData.is_past) {
      return `${Math.abs(countdownData.days_remaining)} giorni fa`;
    } else {
      return `${countdownData.days_remaining} ${countdownData.days_remaining === 1 ? 'giorno' : 'giorni'}`;
    }
  };

  return (
    <div
      style={cardStyle}
      onMouseEnter={(e) => {
        e.currentTarget.style.transform = 'translateY(-4px)';
        e.currentTarget.style.boxShadow = '0 12px 32px rgba(0, 0, 0, 0.2)';
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.transform = 'translateY(0)';
        e.currentTarget.style.boxShadow = '0 8px 24px rgba(0, 0, 0, 0.15)';
      }}
    >
      <div style={eventNameStyle}>
        {countdownData.event_name}
      </div>
      <div style={daysRemainingStyle}>
        {getStatusText()}
      </div>
      <div style={targetDateStyle}>
        {countdownData.target_date}
      </div>
    </div>
  );
};

export default CountdownCard;
