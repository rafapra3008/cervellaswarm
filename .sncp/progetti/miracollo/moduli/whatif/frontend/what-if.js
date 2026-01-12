/**
 * What-If Pricing Simulator
 * Frontend logic with API integration
 */

class WhatIfSimulator {
  constructor() {
    this.apiBaseUrl = 'https://miracollo.com/api/v1';
    this.debounceTimer = null;
    this.currentData = null;

    this.elements = {
      propertySelect: document.getElementById('property-select'),
      dateSelect: document.getElementById('date-select'),
      roomSelect: document.getElementById('room-select'),
      slider: document.getElementById('price-slider'),
      sliderPercentage: document.getElementById('slider-percentage'),
      currentPrice: document.getElementById('current-price'),
      newPrice: document.getElementById('new-price'),
      occupancyBefore: document.getElementById('occupancy-before'),
      occupancyAfter: document.getElementById('occupancy-after'),
      occupancyDelta: document.getElementById('occupancy-delta'),
      revenueBefore: document.getElementById('revenue-before'),
      revenueAfter: document.getElementById('revenue-after'),
      revenueDelta: document.getElementById('revenue-delta'),
      competitorPosition: document.getElementById('competitor-position'),
      competitorAvg: document.getElementById('competitor-avg'),
      confidenceBadge: document.getElementById('confidence-badge'),
      explanationText: document.getElementById('explanation-text'),
      loadingOverlay: document.getElementById('loading-overlay')
    };

    this.init();
  }

  init() {
    // Event listeners
    this.elements.slider.addEventListener('input', (e) => this.handleSliderChange(e));
    this.elements.propertySelect.addEventListener('change', () => this.loadRoomTypes());
    this.elements.dateSelect.addEventListener('change', () => this.resetSimulation());
    this.elements.roomSelect.addEventListener('change', () => this.resetSimulation());

    // Set default date (today + 7 days)
    const futureDate = new Date();
    futureDate.setDate(futureDate.getDate() + 7);
    this.elements.dateSelect.value = futureDate.toISOString().split('T')[0];

    // Load initial data
    this.loadProperties();
  }

  // API Calls
  async loadProperties() {
    try {
      const response = await fetch(`${this.apiBaseUrl}/properties`);

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const properties = await response.json();
      this.populateSelect(this.elements.propertySelect, properties);

    } catch (error) {
      console.error('Error loading properties:', error);
      this.showError('Errore nel caricamento strutture');

      // Fallback: mostra almeno l'interfaccia
      this.populateSelect(this.elements.propertySelect, []);
    }
  }

  async loadRoomTypes() {
    const propertyId = this.elements.propertySelect.value;
    if (!propertyId) return;

    try {
      const response = await fetch(`${this.apiBaseUrl}/properties/${propertyId}/room-types`);

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const roomTypes = await response.json();
      this.populateSelect(this.elements.roomSelect, roomTypes);

    } catch (error) {
      console.error('Error loading room types:', error);
      this.showError('Errore nel caricamento tipologie camera');

      // Fallback: mostra almeno l'interfaccia
      this.populateSelect(this.elements.roomSelect, []);
    }
  }

  async runSimulation(priceAdjustment) {
    const propertyId = this.elements.propertySelect.value;
    const dateTarget = this.elements.dateSelect.value;
    const roomTypeId = this.elements.roomSelect.value;

    if (!propertyId || !dateTarget || !roomTypeId) {
      this.elements.explanationText.textContent =
        'Seleziona struttura, data e tipologia camera per iniziare la simulazione.';
      return;
    }

    this.showLoading(true);

    try {
      const response = await fetch(`${this.apiBaseUrl}/what-if/simulate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          property_id: parseInt(propertyId),
          date_target: dateTarget,
          room_type_id: parseInt(roomTypeId),
          price_adjustment: priceAdjustment
        })
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();
      this.currentData = data;
      this.updateUI(data);

    } catch (error) {
      console.error('Simulation error:', error);
      this.showError('Errore nella simulazione. Riprova.');
    } finally {
      this.showLoading(false);
    }
  }

  // UI Updates
  handleSliderChange(event) {
    const percentage = parseInt(event.target.value);
    const adjustment = percentage / 100;

    this.elements.sliderPercentage.textContent = `${percentage > 0 ? '+' : ''}${percentage}%`;

    // Debounce API call
    clearTimeout(this.debounceTimer);
    this.debounceTimer = setTimeout(() => {
      this.runSimulation(adjustment);
    }, 300);
  }

  updateUI(data) {
    // Prices
    this.elements.currentPrice.textContent = this.formatPrice(data.current_price);
    this.elements.newPrice.textContent = this.formatPrice(data.new_price);

    // Occupancy
    this.elements.occupancyBefore.textContent = this.formatPercentage(data.current_occupancy);
    this.elements.occupancyAfter.textContent = this.formatPercentage(data.predicted_occupancy);
    this.updateDelta(
      this.elements.occupancyDelta,
      data.occupancy_delta,
      this.formatPercentage
    );

    // Revenue
    this.elements.revenueBefore.textContent = this.formatRevenue(data.current_revenue);
    this.elements.revenueAfter.textContent = this.formatRevenue(data.predicted_revenue);
    this.updateDelta(
      this.elements.revenueDelta,
      data.revenue_delta,
      this.formatRevenue
    );

    // Competitor
    this.updateCompetitorPosition(data.competitor_position);
    this.elements.competitorAvg.textContent = this.formatPrice(data.competitor_avg);

    // Confidence
    this.updateConfidence(data.confidence);

    // Explanation
    this.elements.explanationText.textContent = data.explanation;
  }

  updateDelta(element, value, formatter) {
    const deltaValue = element.querySelector('.delta-value');

    element.className = 'impact-delta';
    if (value > 0) {
      element.classList.add('positive');
      deltaValue.textContent = `+${formatter(Math.abs(value))}`;
    } else if (value < 0) {
      element.classList.add('negative');
      deltaValue.textContent = `-${formatter(Math.abs(value))}`;
    } else {
      element.classList.add('neutral');
      deltaValue.textContent = formatter(0);
    }
  }

  updateCompetitorPosition(position) {
    const positionEl = this.elements.competitorPosition;
    const badge = positionEl.querySelector('.position-badge');

    badge.textContent = position;
    badge.className = `position-badge ${position}`;
  }

  updateConfidence(confidence) {
    const badge = this.elements.confidenceBadge;
    badge.textContent = confidence;
    badge.className = `confidence-badge ${confidence}`;
  }

  resetSimulation() {
    this.elements.slider.value = 0;
    this.elements.sliderPercentage.textContent = '0%';

    // Reset display
    this.elements.occupancyDelta.className = 'impact-delta neutral';
    this.elements.revenueDelta.className = 'impact-delta neutral';
    this.elements.explanationText.textContent =
      'Muovi lo slider per simulare un cambio prezzo e vedere l\'impatto previsto.';
  }

  // Utilities
  populateSelect(selectElement, items) {
    // Keep first option (placeholder)
    while (selectElement.options.length > 1) {
      selectElement.remove(1);
    }

    items.forEach(item => {
      const option = document.createElement('option');
      option.value = item.id;
      option.textContent = item.name;
      selectElement.appendChild(option);
    });
  }

  formatPrice(value) {
    return `€${value.toFixed(2)}`;
  }

  formatPercentage(value) {
    return `${(value * 100).toFixed(0)}%`;
  }

  formatRevenue(value) {
    return `€${value.toLocaleString('it-IT', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`;
  }

  showLoading(show) {
    this.elements.loadingOverlay.style.display = show ? 'flex' : 'none';
  }

  showError(message) {
    this.elements.explanationText.textContent = `⚠️ ${message}`;
    this.elements.confidenceBadge.textContent = 'error';
    this.elements.confidenceBadge.className = 'confidence-badge low';
  }
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  window.whatIfSimulator = new WhatIfSimulator();
});
