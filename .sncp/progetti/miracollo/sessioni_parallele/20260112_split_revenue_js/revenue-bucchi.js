/**
 * Revenue Intelligence Dashboard - Miracollo
 * BUCCHI: Fetch and render bucchi, occupancy
 * Split from revenue.js
 */

// Fetch bucchi
async function fetchBucchi() {
    const response = await fetch(`${API_BASE}/bucchi?hotel_code=${hotelCode}&finestra=${currentFinestra}`);
    if (!response.ok) throw new Error('Fetch bucchi failed');
    const data = await response.json();
    if (DEBUG_REVENUE) console.log("[Bucchi] API response:", { total: data.total, items: (data.bucchi || []).length });
    return data;
}

// Fetch occupancy forecast
async function fetchOccupancyForecast() {
    try {
        // Calcola date range (prossimi 30 giorni)
        const today = new Date();
        const endDate = new Date(today);
        endDate.setDate(endDate.getDate() + 30);

        const startDateStr = today.toISOString().split('T')[0];
        const endDateStr = endDate.toISOString().split('T')[0];

        const response = await fetch(
            `${API_BASE}/occupancy-forecast?hotel_code=${hotelCode}&start_date=${startDateStr}&end_date=${endDateStr}`
        );

        if (!response.ok) {
            console.warn('Occupancy forecast endpoint non disponibile');
            return { summary: { occupancy_media: null } };
        }
        const data = await response.json();
        if (DEBUG_REVENUE) console.log("[Occupancy] API response:", data);
        return data;
    } catch (error) {
        console.error('Error fetching occupancy forecast:', error);
        return { summary: { occupancy_media: null } };
    }
}

// Update overview cards
function updateOverview(data) {
    const summary = data.summary || {};

    // Bucchi count
    document.getElementById('bucchi-count').textContent = summary.totale_bucchi || 0;

    // Impatto
    const impatto = summary.impatto_euro_totale || 0;
    document.getElementById('impatto-value').textContent = `€${impatto.toLocaleString()}`;

    // Update badges per finestra
    updateBadges(data);
}

// Update tab badges
function updateBadges(data) {
    const badge = document.getElementById(`badge-${currentFinestra}`);
    if (badge) {
        badge.textContent = data.summary?.totale_bucchi || 0;
    }
}

// Update occupancy card
function updateOccupancy(data) {
    const occupancyMedia = data.summary?.occupancy_media;

    // Calcola target medio (70% default basato su design)
    const targetMedio = 70;

    // Update DOM
    const occValue = document.getElementById('occupancy-value');
    const occTarget = document.getElementById('occupancy-target');

    if (occValue) {
        occValue.textContent = occupancyMedia !== null ? `${occupancyMedia}%` : '--%';
    }
    if (occTarget) {
        occTarget.textContent = targetMedio;
    }

    if (DEBUG_REVENUE) console.log('Occupancy updated:', { media: occupancyMedia, target: targetMedio });
}

// Render bucchi list
function renderBucchi(data) {
    const container = document.getElementById('bucchi-list');
    const bucchi = data.bucchi || [];

    if (bucchi.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="emoji">✅</div>
                <div>Nessun bucco! Tutto sotto controllo.</div>
            </div>
        `;
        return;
    }

    container.innerHTML = bucchi.slice(0, 5).map((bucco, index) => `
        <div class="bucco-card"
             data-urgenza="${escapeHtml(bucco.urgenza)}"
             data-bucco-id="bucco_${index}"
             onclick="toggleBuccoDetails('bucco_${index}')"
             style="cursor: pointer;">
            <div class="bucco-header">
                <div>
                    <span class="bucco-badge">${escapeHtml(bucco.urgenza)}</span>
                </div>
                <span class="bucco-expand-icon">▼</span>
            </div>
            <div class="bucco-date">${formatDateRange(bucco.data_inizio, bucco.data_fine)} (${bucco.giorni}gg)</div>
            <div class="bucco-metrics">
                <span>📦 ${bucco.camere_vuote} camere vuote</span>
                <span>📉 gap ${bucco.gap_medio}%</span>
                <span>💶 €${bucco.impatto_euro.toLocaleString()} a rischio</span>
            </div>
            <div class="bucco-details" id="details_bucco_${index}" style="display: none; margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #e5e7eb;">
                <div style="font-size: 0.85rem; color: #6b7280;">
                    <p><strong>Periodo:</strong> ${formatDateRange(bucco.data_inizio, bucco.data_fine)}</p>
                    <p><strong>Camere disponibili:</strong> ${bucco.camere_vuote}</p>
                    <p><strong>Gap vs target:</strong> ${bucco.gap_medio}%</p>
                    <p><strong>Impatto stimato:</strong> €${bucco.impatto_euro.toLocaleString()}</p>
                    ${bucco.motivo ? `<p><strong>Motivo:</strong> ${escapeHtml(bucco.motivo)}</p>` : ''}
                </div>
            </div>
        </div>
    `).join('');
}

// Toggle bucco details
function toggleBuccoDetails(buccoId) {
    const details = document.getElementById('details_' + buccoId);
    const card = document.querySelector(`[data-bucco-id="${buccoId}"]`);
    const icon = card?.querySelector('.bucco-expand-icon');

    if (details) {
        const isHidden = details.style.display === 'none';
        details.style.display = isHidden ? 'block' : 'none';
        if (icon) {
            icon.textContent = isHidden ? '▲' : '▼';
        }
        if (DEBUG_REVENUE) console.log('Bucco details toggled:', buccoId, isHidden ? 'expanded' : 'collapsed');
    }
}
