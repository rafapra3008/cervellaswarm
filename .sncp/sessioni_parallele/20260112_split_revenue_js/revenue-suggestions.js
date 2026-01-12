/**
 * Revenue Intelligence Dashboard - Miracollo
 * SUGGESTIONS: Fetch, render suggestions, confidence, what-if
 * Split from revenue.js
 */

// Fetch suggestions
async function fetchSuggestions() {
    const response = await fetch(`${API_BASE}/suggestions?hotel_code=${hotelCode}&limit=10`);
    if (!response.ok) throw new Error('Fetch suggestions failed');
    const data = await response.json();
    if (DEBUG_REVENUE) console.log("[Suggestions] API response:", { total: data.total, items: (data.suggestions || []).length });
    return data;
}

// Helper per confidence badge con tooltip
function renderConfidenceBadge(score, level) {
    if (score === undefined && score !== 0) return '';

    const icons = {
        'alta': '✓',
        'molto_alta': '✓',
        'media': '⚠',
        'bassa': '✗',
        'molto_bassa': '✗'
    };

    // Normalizza level per classe CSS
    let levelClass = 'media';
    let levelDisplay = 'Media';
    if (level) {
        const l = level.toLowerCase();
        if (l.includes('alta')) {
            levelClass = 'alta';
            levelDisplay = l === 'molto_alta' ? 'Molto Alta' : 'Alta';
        } else if (l.includes('bassa')) {
            levelClass = 'bassa';
            levelDisplay = l === 'molto_bassa' ? 'Molto Bassa' : 'Bassa';
        } else {
            levelDisplay = 'Media';
        }
    }

    const icon = icons[level?.toLowerCase()] || '○';
    const displayScore = Math.round(score || 0);

    // Genera spiegazione basata sul livello
    let explanation = 'Basato su pattern storici e dati di vendita simili.';
    if (levelClass === 'alta') {
        explanation = 'Alta affidabilità basata su molti dati storici coerenti.';
    } else if (levelClass === 'bassa') {
        explanation = 'Pochi dati disponibili. Valuta manualmente prima di applicare.';
    }

    // ID unico per ogni badge
    const badgeId = 'badge_' + Math.random().toString(36).substr(2, 9);

    return `
        <div class="confidence-badge-wrapper">
            <div class="confidence-badge confidence-${levelClass}">
                <span class="confidence-icon">${icon}</span>
                <span>${displayScore}%</span>
            </div>
            <div class="confidence-tooltip" id="${badgeId}">
                <div class="tooltip-header">
                    <span>🤖</span>
                    <span>Affidabilità AI</span>
                </div>
                <div class="tooltip-row">
                    <span class="tooltip-label">Score</span>
                    <span class="tooltip-value">${displayScore}%</span>
                </div>
                <div class="tooltip-row">
                    <span class="tooltip-label">Livello</span>
                    <span class="tooltip-value">${levelDisplay}</span>
                </div>
                <div class="tooltip-info">
                    <span class="tooltip-info-icon">ℹ️</span>
                    ${explanation}
                </div>
                <div class="ml-details-link" onclick="toggleMLDetails('${badgeId}', event)">
                    Dettagli modello ↓
                </div>
                <div class="ml-details-panel" id="panel_${badgeId}">
                    <div class="ml-details-loading">Caricamento...</div>
                </div>
            </div>
        </div>
    `;
}

// Toggle ML details panel
async function toggleMLDetails(badgeId, event) {
    event.stopPropagation();

    const panel = document.getElementById('panel_' + badgeId);
    const link = event.target;
    const tooltip = document.getElementById(badgeId);

    if (!panel) return;

    const isExpanded = panel.classList.contains('expanded');

    if (isExpanded) {
        // Collapse
        panel.classList.remove('expanded');
        link.textContent = 'Dettagli modello ↓';
        tooltip?.classList.remove('keep-open');
    } else {
        // Expand
        panel.classList.add('expanded');
        link.textContent = 'Chiudi ↑';
        tooltip?.classList.add('keep-open');

        // Load model info if not already loaded
        if (panel.querySelector('.ml-details-loading')) {
            await loadMLDetails(panel);
        }
    }
}

// Load ML model details
async function loadMLDetails(panel) {
    try {
        // Map hotel code to hotel_id (for now hardcoded to 1)
        const hotelId = 1; // TODO: get from hotel code mapping
        const response = await fetch(`/api/ml/model-info?hotel_id=${hotelId}`);

        if (!response.ok) {
            panel.innerHTML = '<div class="ml-details-error">Dati non disponibili</div>';
            return;
        }

        const data = await response.json();

        // Format trained_at as "X giorni fa"
        const trainedAt = new Date(data.trained_at);
        const now = new Date();
        const daysAgo = Math.floor((now - trainedAt) / (1000 * 60 * 60 * 24));
        const trainedText = daysAgo === 0 ? 'oggi' :
                           daysAgo === 1 ? 'ieri' :
                           `${daysAgo} giorni fa`;

        // Get top 3 features
        const featureImportance = data.feature_importance || {};
        const topFeatures = Object.entries(featureImportance)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 3);

        // Render details
        const metrics = data.metrics || {};
        const samples = data.samples || {};

        panel.innerHTML = `
            <div class="ml-details-header">Dettagli Modello ML</div>
            <div class="ml-details-grid">
                <div class="ml-detail-item">
                    <span class="ml-detail-label">R² Score:</span>
                    <span class="ml-detail-value">${(metrics.r2_score || 0).toFixed(3)}</span>
                </div>
                <div class="ml-detail-item">
                    <span class="ml-detail-label">Samples:</span>
                    <span class="ml-detail-value">${samples.total || 0}</span>
                </div>
                <div class="ml-detail-item">
                    <span class="ml-detail-label">Features:</span>
                    <span class="ml-detail-value">${data.n_features || 0}</span>
                </div>
                <div class="ml-detail-item">
                    <span class="ml-detail-label">Ultimo Train:</span>
                    <span class="ml-detail-value">${trainedText}</span>
                </div>
            </div>
            <div class="ml-features">
                <div class="ml-features-label">Top Features:</div>
                ${topFeatures.map(([name, importance]) => `
                    <div class="ml-feature-item">
                        <span class="ml-feature-name">• ${formatFeatureName(name)}</span>
                        <span class="ml-feature-importance">(${Math.round(importance * 100)}%)</span>
                    </div>
                `).join('')}
            </div>
        `;
    } catch (error) {
        console.error('Error loading ML details:', error);
        panel.innerHTML = '<div class="ml-details-error">Errore caricamento dati</div>';
    }
}

// Format feature name for display
function formatFeatureName(name) {
    // Convert snake_case to readable format
    return name
        .replace(/_/g, ' ')
        .replace(/\b\w/g, l => l.toUpperCase());
}

// NOTE: formatDateRange() is in revenue-core.js (loaded first)

// Render suggestions
function renderSuggestions(data) {
    const container = document.getElementById('suggerimenti-list');
    const suggestions = data.suggestions || [];

    if (suggestions.length === 0) {
        container.innerHTML = '<div class="empty-state">Nessun suggerimento al momento</div>';
        return;
    }

    const icons = {
        prezzo: '💰',
        promozione: '🏷️',
        upgrade: '⬆️',
        pacchetto: '🎁',
        marketing: '📢'
    };

    container.innerHTML = suggestions.slice(0, 5).map((sugg, index) => {
        const suggId = `sugg_${index}_${sugg.id}`;

        return `
        <div class="suggerimento-card" data-sugg-id="${suggId}">
            <div class="suggerimento-tipo" data-tipo="${escapeHtml(sugg.tipo)}">
                ${icons[sugg.tipo] || '💡'}
            </div>
            <div class="suggerimento-content">
                <div class="suggerimento-azione">${escapeHtml(sugg.azione)}</div>
                <div class="suggerimento-motivo">${escapeHtml(sugg.motivazione)}</div>
            </div>
            <div class="suggerimento-priorita">${sugg.priorita}%</div>
            ${renderConfidenceBadge(sugg.confidence_score, sugg.confidence_level)}
            <button class="btn-action btn-secondary btn-whatif"
                    onclick="toggleWhatIfPanel('${suggId}', ${sugg.suggested_price || 0})">
                🔮 Simula
            </button>
            <button class="btn-action btn-primary"
                    onclick="applySuggestion('${escapeHtml(sugg.id)}', '${escapeHtml(sugg.bucco_id || '')}')">
                Applica
            </button>
            <div class="what-if-panel" id="whatif_${suggId}"></div>
        </div>
    `;
    }).join('');
}

// ============================================
// WHAT-IF SIMULATION
// ============================================

// Toggle What-If simulation panel
async function toggleWhatIfPanel(suggId, basePrice) {
    const panel = document.getElementById(`whatif_${suggId}`);
    const card = document.querySelector(`[data-sugg-id="${suggId}"]`);

    if (!panel || !card) return;

    const isExpanded = panel.classList.contains('expanded');

    if (isExpanded) {
        // Collapse panel
        panel.classList.remove('expanded');
        panel.innerHTML = '';
    } else {
        // Expand panel
        panel.classList.add('expanded');
        panel.innerHTML = '<div class="what-if-loading">Simulazione in corso...</div>';

        // Load what-if data
        await loadWhatIfData(panel, basePrice);
    }
}

// Load What-If simulation data
async function loadWhatIfData(panel, basePrice) {
    try {
        const hotelId = 1; // TODO: map from hotelCode

        // Genera scenari di sconto
        const scenarios = [
            { label: '-10%', discount_pct: 10 },
            { label: '-15%', discount_pct: 15 },
            { label: '-20%', discount_pct: 20 },
            { label: '-25%', discount_pct: 25 }
        ];

        const response = await fetch(`/api/ml/what-if?hotel_id=${hotelId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                base_suggestion: {
                    price: basePrice,
                    discount_pct: 0
                },
                scenarios: scenarios
            })
        });

        if (!response.ok) {
            panel.innerHTML = '<div class="what-if-error">Simulazione non disponibile</div>';
            return;
        }

        const data = await response.json();
        renderWhatIfPanel(panel, data, basePrice);

    } catch (error) {
        console.error('Error loading what-if data:', error);
        panel.innerHTML = '<div class="what-if-error">Errore durante simulazione</div>';
    }
}

// Render What-If panel
function renderWhatIfPanel(panel, data, basePrice) {
    const base = data.base || {};
    const scenarios = data.scenarios || [];

    // Trova scenario migliore
    const best = scenarios.reduce((acc, s) =>
        (s.predicted_performance || 0) > (acc.predicted_performance || 0) ? s : acc,
        scenarios[0] || {}
    );

    const rowsHtml = scenarios.map(scenario => {
        const performance = scenario.predicted_performance || 0;
        const delta = scenario.delta_vs_base || 0;
        const isBest = scenario === best;
        const price = Math.round(basePrice * (1 - scenario.discount_pct / 100));

        // Colore delta
        let deltaClass = 'neutral';
        if (delta > 0) deltaClass = 'positive';
        else if (delta < 0) deltaClass = 'negative';

        return `
            <tr class="what-if-row ${isBest ? 'what-if-row-best' : ''}">
                <td class="what-if-scenario">
                    ${scenario.label} (€${price})
                    ${isBest ? '<span class="what-if-best-badge">⭐ MIGLIORE</span>' : ''}
                </td>
                <td class="what-if-performance">${performance.toFixed(0)}%</td>
                <td class="what-if-delta what-if-delta-${deltaClass}">
                    ${delta > 0 ? '+' : ''}${delta.toFixed(1)}%
                </td>
                <td class="what-if-actions">
                    <button class="btn-whatif-apply"
                            onclick="applyWhatIfScenario(${price}, '${scenario.label}')">
                        Applica
                    </button>
                </td>
            </tr>
        `;
    }).join('');

    panel.innerHTML = `
        <div class="what-if-content">
            <div class="what-if-header">
                <span>💡 Simula Altri Sconti</span>
                <button class="what-if-close" onclick="closeWhatIfPanel(this)">×</button>
            </div>
            <table class="what-if-table">
                <thead>
                    <tr>
                        <th>Scenario</th>
                        <th>Performance</th>
                        <th>vs Base</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    ${rowsHtml}
                </tbody>
            </table>
            <div class="what-if-footer">
                <span class="what-if-info">ℹ️ Previsioni basate su modello ML</span>
            </div>
        </div>
    `;
}

// Close What-If panel
function closeWhatIfPanel(buttonEl) {
    const panel = buttonEl.closest('.what-if-panel');
    if (panel) {
        panel.classList.remove('expanded');
        setTimeout(() => panel.innerHTML = '', 300);
    }
}

// Apply What-If scenario
async function applyWhatIfScenario(price, scenarioLabel) {
    showToast(`Applicando scenario ${scenarioLabel}: €${price}`, 'success');
    // TODO: Implementare logica per applicare il prezzo simulato
    // Potrebbe essere un update diretto del prezzo o generare un nuovo suggerimento
    if (DEBUG_REVENUE) console.log('Apply What-If scenario:', { price, scenarioLabel });
}
