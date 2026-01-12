/**
 * Revenue Intelligence Dashboard - Miracollo
 * CHARTS: Eventi, Booking Pace, Price History
 * Split from revenue.js
 */

// ============================================
// EVENTI LOCALI
// ============================================

// Fetch eventi locali
async function fetchEventi() {
    try {
        // Calcola date range (prossimi 30 giorni)
        const today = new Date();
        const endDate = new Date(today);
        endDate.setDate(endDate.getDate() + 30);

        const startDateStr = today.toISOString().split('T')[0];
        const endDateStr = endDate.toISOString().split('T')[0];

        const response = await fetch(
            `${API_BASE}/events?hotel_code=${hotelCode}&start_date=${startDateStr}&end_date=${endDateStr}`
        );

        if (!response.ok) {
            console.warn('Eventi endpoint non disponibile');
            return { events: [] };
        }

        const data = await response.json();
        if (DEBUG_REVENUE) console.log("[Eventi] API response:", { total: data.total, items: (data.events || []).length });
        return data;
    } catch (error) {
        console.error('Error fetching eventi:', error);
        return { events: [] };
    }
}

// Render eventi locali
function renderEventi(data) {
    const container = document.getElementById('eventi-list');
    const eventi = data.events || [];

    if (eventi.length === 0) {
        container.innerHTML = `
            <div class="empty-state" style="padding: 2rem 1rem;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📅</div>
                <div style="font-size: 0.85rem;">Nessun evento in programma</div>
            </div>
        `;
        return;
    }

    const iconMap = {
        concerto: '🎵',
        fiera: '🎪',
        festival: '🎉',
        sport: '⚽',
        conferenza: '🎤',
        default: '📅'
    };

    container.innerHTML = eventi.slice(0, 5).map(evento => {
        const icon = iconMap[evento.tipo?.toLowerCase()] || iconMap.default;
        const dataFormattata = new Date(evento.data).toLocaleDateString('it-IT', {
            day: 'numeric',
            month: 'short'
        });

        return `
            <div class="evento-card">
                <div class="evento-icon">${icon}</div>
                <div class="evento-content">
                    <div class="evento-nome" title="${escapeHtml(evento.nome)}">
                        ${escapeHtml(evento.nome)}
                    </div>
                    <div class="evento-meta">
                        <span>📍 ${dataFormattata}</span>
                        ${evento.distanza_km ? `<span>🚗 ${evento.distanza_km}km</span>` : ''}
                    </div>
                </div>
                ${evento.impatto_stimato ? `
                    <div class="evento-impatto">${escapeHtml(evento.impatto_stimato)}</div>
                ` : ''}
            </div>
        `;
    }).join('');
}

// ============================================
// BOOKING PACE
// ============================================

// Fetch booking pace
async function fetchBookingPace() {
    try {
        const response = await fetch(
            `${API_BASE}/research?hotel_code=${hotelCode}`
        );

        if (!response.ok) {
            console.warn('Booking pace endpoint non disponibile');
            return { data: null };
        }

        const json = await response.json();
        if (DEBUG_REVENUE) console.log('Booking pace API response:', json);
        // L'API ritorna booking_pace dentro il JSON principale
        return { data: json.booking_pace || null };
    } catch (error) {
        console.error('Error fetching booking pace:', error);
        return { data: null };
    }
}

// Render booking pace
function renderBookingPace(data) {
    const container = document.getElementById('booking-pace-content');
    const paceData = data.data;

    if (!paceData) {
        container.innerHTML = `
            <div class="empty-state" style="padding: 2rem 1rem;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📊</div>
                <div style="font-size: 0.85rem;">Dati booking pace non disponibili</div>
            </div>
        `;
        return;
    }

    // Estrai metriche dalla struttura corretta dell'API
    const currentPace = paceData.corrente?.prenotazioni || 0;
    const previousPace = paceData.anno_scorso?.prenotazioni || 0;
    const variazione = paceData.delta?.percentuale || 0;

    if (DEBUG_REVENUE) console.log('Booking pace metrics:', { currentPace, previousPace, variazione });

    const isPositive = variazione > 0;
    const isNegative = variazione < 0;
    const indicatorClass = isPositive ? 'positive' : isNegative ? 'negative' : 'neutral';
    const trendIcon = isPositive ? '📈' : isNegative ? '📉' : '➡️';
    const arrow = isPositive ? '↑' : isNegative ? '↓' : '→';

    container.innerHTML = `
        <div class="pace-card">
            <div class="pace-header">
                <div class="pace-label">Prenotazioni YTD</div>
                <div class="pace-trend">${trendIcon}</div>
            </div>
            <div class="pace-value">
                <div class="pace-number">${currentPace}</div>
                <div class="pace-vs">vs ${previousPace} (2025)</div>
            </div>
            <div class="pace-indicator ${indicatorClass}">
                <span>${arrow}</span>
                <span>${Math.abs(variazione)}%</span>
            </div>
            <div class="pace-description">
                ${isPositive
                    ? `Ritmo prenotazioni superiore del ${variazione}% rispetto allo stesso periodo dell'anno scorso.`
                    : isNegative
                    ? `Ritmo prenotazioni inferiore del ${Math.abs(variazione)}% rispetto allo stesso periodo dell'anno scorso.`
                    : 'Ritmo prenotazioni in linea con lo stesso periodo dell\'anno scorso.'
                }
            </div>
        </div>
    `;
}

// ============================================
// PRICE HISTORY
// ============================================

// Fetch price history
async function fetchPriceHistory() {
    if (DEBUG_REVENUE) console.log("[PriceHistory] Fetching for hotel:", hotelCode);
    try {
        const response = await fetch(
            `/api/pricing/history?hotel_code=${hotelCode}&days=30`
        );

        if (!response.ok) {
            console.warn('Price history endpoint non disponibile');
            return { changes: [] };
        }

        const data = await response.json();
        if (DEBUG_REVENUE) console.log("[PriceHistory] API response:", { total: data.total, items: (data.timeline || data.changes || []).length });
        return data;
    } catch (error) {
        console.error('Error fetching price history:', error);
        return { changes: [] };
    }
}

// Render price history
function renderPriceHistory(data) {
    if (DEBUG_REVENUE) console.log("[PriceHistory] Rendering:", { total: data?.total, changes: (data?.timeline || data?.changes || []).length });
    const timelineWrapper = document.getElementById('price-timeline-wrapper');
    const changesListContainer = document.getElementById('price-changes-list');
    const changes = data.timeline || data.changes || [];

    // Se nessun dato
    if (changes.length === 0) {
        timelineWrapper.innerHTML = `
            <div class="empty-state" style="padding: 2rem 1rem;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📊</div>
                <div style="font-size: 0.85rem;">Nessun cambio prezzo negli ultimi 30 giorni</div>
            </div>
        `;
        changesListContainer.innerHTML = '';
        return;
    }

    // Render timeline
    renderPriceTimeline(changes, timelineWrapper);

    // Render changes list
    renderPriceChangesList(changes, changesListContainer);
}

// Render price timeline
function renderPriceTimeline(changes, container) {
    // Trova min/max prezzi per scalare il grafico
    const prices = changes.map(c => c.new_price);
    const minPrice = Math.min(...prices);
    const maxPrice = Math.max(...prices);
    const priceRange = maxPrice - minPrice;
    const padding = priceRange * 0.1; // 10% padding

    const yMin = Math.floor(minPrice - padding);
    const yMax = Math.ceil(maxPrice + padding);
    const yRange = yMax - yMin;

    // Genera 5 tick labels per Y axis
    const yTicks = [];
    for (let i = 0; i < 5; i++) {
        const value = yMax - (yRange * i / 4);
        yTicks.push(Math.round(value));
    }

    // Calcola posizioni markers
    const canvasHeight = 150; // px
    const canvasWidth = 100; // %

    // Ordina changes per data
    const sortedChanges = [...changes].sort((a, b) =>
        new Date(a.date.replace(' ', 'T')) - new Date(b.date.replace(' ', 'T'))
    );

    // Calcola timeline range (30 giorni)
    const today = new Date();
    const startDate = new Date(today);
    startDate.setDate(startDate.getDate() - 30);

    const markersHtml = sortedChanges.map(change => {
        const changeDate = new Date(change.date.replace(' ', 'T'));
        const daysFromStart = (changeDate - startDate) / (1000 * 60 * 60 * 24);
        const xPercent = (daysFromStart / 30) * 100;

        const pricePosition = (change.new_price - yMin) / yRange;
        const yPercent = (1 - pricePosition) * 100;

        const markerClass = change.change_type === 'AI_APPLIED' ? 'ai-applied' : 'manual';

        return `
            <div class="price-change-marker ${markerClass}"
                 style="left: ${xPercent}%; bottom: ${100 - yPercent}%;"
                 title="${formatDateShort(change.date)}: €${change.new_price}">
            </div>
        `;
    }).join('');

    container.innerHTML = `
        <div class="price-timeline">
            <div class="price-timeline-grid">
                <div class="price-timeline-y-axis">
                    ${yTicks.map(tick => `<div>€${tick}</div>`).join('')}
                </div>
                <div class="price-timeline-canvas">
                    ${markersHtml}
                </div>
            </div>
            <div class="price-timeline-legend">
                <div class="legend-item">
                    <div class="legend-marker ai"></div>
                    <span>AI Applied</span>
                </div>
                <div class="legend-item">
                    <div class="legend-marker manual"></div>
                    <span>Manual</span>
                </div>
            </div>
        </div>
    `;
}

// Render price changes list
function renderPriceChangesList(changes, container) {
    // Ordina per data (più recente prima)
    const sortedChanges = [...changes].sort((a, b) =>
        new Date(b.date.replace(' ', 'T')) - new Date(a.date.replace(' ', 'T'))
    );

    // Mostra max 5 cambi recenti
    const recentChanges = sortedChanges.slice(0, 5);

    const changesHtml = recentChanges.map(change => {
        const badge = change.change_type === 'AI_APPLIED' ?
            '<span class="price-change-badge ai">AI</span>' :
            '<span class="price-change-badge manual">Manual</span>';

        const performanceBadge = renderPerformanceBadge(change);

        return `
            <div class="price-change-item">
                <div class="price-change-date">${formatDateShort(change.date)}</div>
                <div class="price-change-values">
                    €${change.old_price}<span class="price-change-arrow">→</span>€${change.new_price}
                </div>
                ${badge}
                ${performanceBadge}
            </div>
        `;
    }).join('');

    container.innerHTML = `
        <div class="price-changes-header">Recent Changes</div>
        ${changesHtml}
    `;
}

// Render performance badge
function renderPerformanceBadge(change) {
    if (!change.performance_status) return '';

    const statusClass = getStatusColor(change.performance_status);
    const statusIcon = {
        SUCCESS: '✓',
        NEUTRAL: '○',
        WARNING: '!',
        FAILURE: '✗'
    }[change.performance_status] || '○';

    let statusText = '';
    if (change.revenue_delta_pct !== null && change.revenue_delta_pct !== undefined) {
        const sign = change.revenue_delta_pct > 0 ? '+' : '';
        statusText = `${sign}${change.revenue_delta_pct.toFixed(1)}%`;
    }

    return `
        <span class="performance-badge badge-${statusClass}">
            ${statusIcon} ${statusText}
        </span>
    `;
}

// Get status color class
function getStatusColor(status) {
    const colorMap = {
        SUCCESS: 'success',
        NEUTRAL: 'neutral',
        WARNING: 'warning',
        FAILURE: 'failure'
    };
    return colorMap[status] || 'neutral';
}

// Format date short
function formatDateShort(dateStr) {
    const date = new Date(dateStr.replace(" ", "T"));
    return date.toLocaleDateString('it-IT', { day: 'numeric', month: 'short' });
}
