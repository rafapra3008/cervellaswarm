/**
 * Revenue Intelligence Dashboard - Miracollo
 * CORE: Config, Init, Helpers
 * Split from revenue.js
 */

// Config
const DEBUG_REVENUE = false;  // Set to true for debug logs
const API_BASE = '/api/revenue';
let currentFinestra = '1_settimana';
let hotelCode = 'NL';
let refreshIntervalId = null;

// Security helper - Escape HTML per prevenire XSS
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Toast notification system
function showToast(message, type = 'success') {
    // Rimuovi toast precedenti
    const existing = document.querySelector('.toast');
    if (existing) existing.remove();

    // Crea toast
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 12px 24px;
        border-radius: 8px;
        background: ${type === 'error' ? '#ef4444' : type === 'warning' ? '#f59e0b' : '#10b981'};
        color: white;
        font-weight: 500;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 9999;
        animation: slideIn 0.3s ease-out;
    `;

    document.body.appendChild(toast);

    // Auto-remove - durata dipende dal tipo
    const duration = type === 'error' ? 7000 : type === 'warning' ? 5000 : 5000;
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease-in';
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

// Show loading state
function showLoading() {
    document.getElementById('bucchi-list').innerHTML = '<div class="loading">Caricamento...</div>';
    document.getElementById('suggerimenti-list').innerHTML = '<div class="loading">Caricamento...</div>';
    document.getElementById('eventi-list').innerHTML = '<div class="loading">Caricamento...</div>';
    document.getElementById('booking-pace-content').innerHTML = '<div class="loading">Caricamento...</div>';
    document.getElementById('price-timeline-wrapper').innerHTML = '<div class="loading">Caricamento...</div>';
    document.getElementById('price-changes-list').innerHTML = '<div class="loading">Caricamento...</div>';
}

// Show error state
function showError(msg) {
    document.getElementById('bucchi-list').innerHTML = `<div class="empty-state">${msg}</div>`;
    document.getElementById('suggerimenti-list').innerHTML = `<div class="empty-state">${msg}</div>`;
}

// Cambia finestra temporale
function cambiaFinestra(finestra) {
    currentFinestra = finestra;

    // Update tabs
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.finestra === finestra);
    });

    loadData();
}

// Load all data
async function loadData() {
    try {
        showLoading();

        // Load bucchi
        const bucchiData = await fetchBucchi();
        renderBucchi(bucchiData);
        updateOverview(bucchiData);

        // Load suggestions
        const suggData = await fetchSuggestions();
        renderSuggestions(suggData);

        // Load occupancy forecast
        const occData = await fetchOccupancyForecast();
        updateOccupancy(occData);

        // Load eventi locali
        const eventiData = await fetchEventi();
        renderEventi(eventiData);

        // Load booking pace
        const paceData = await fetchBookingPace();
        renderBookingPace(paceData);

        // Load price history
        const priceData = await fetchPriceHistory();
        renderPriceHistory(priceData);

        // Check AI performance alerts
        const aiHealth = await fetchAIHealth();
        checkPerformanceAlerts(aiHealth);

        // Update timestamp
        document.getElementById('lastUpdate').textContent =
            `Ultimo agg: ${new Date().toLocaleTimeString('it-IT', {hour: '2-digit', minute: '2-digit'})}`;

    } catch (error) {
        console.error('Error loading data:', error);
        showError('Errore caricamento dati');
    }
}

// Refresh data
function refreshData() {
    loadData();
}

// Format date range (usata da bucchi e altri)
function formatDateRange(start, end) {
    const s = new Date(start);
    const e = new Date(end);
    const opts = { day: 'numeric', month: 'short' };

    if (start === end) {
        return s.toLocaleDateString('it-IT', opts);
    }
    return `${s.toLocaleDateString('it-IT', opts)} - ${e.toLocaleDateString('it-IT', opts)}`;
}
