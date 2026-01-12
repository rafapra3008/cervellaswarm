/**
 * Revenue Intelligence Dashboard - Miracollo
 * ACTIONS: Apply, Undo, AI Health, Monitoring
 * Split from revenue.js
 */

// Apply suggestion
async function applySuggestion(id, buccoId) {
    try {
        if (DEBUG_REVENUE) console.log('Applying suggestion:', { id, buccoId });

        const response = await fetch(`${API_BASE}/suggestions/${id}/action?hotel_code=${hotelCode}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                action: 'accept',
                bucco_id: buccoId || null
            })
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.message || 'Errore applicazione suggerimento');
        }

        const responseData = await response.json();
        if (DEBUG_REVENUE) console.log('Suggestion applied successfully:', { id, response: responseData });

        // ACTION TRACKING: Mostra conferma con undo
        if (window.ActionTracking) {
            // Estrai info dalla risposta
            const actionInfo = responseData.action_details || responseData.action || {};
            const applicationId = responseData.application_id || null;
            const notti = actionInfo.dates_updated || actionInfo.notti || 14;
            const prezzoPrima = actionInfo.price_before || actionInfo.prezzo_prima || 120;
            const prezzoDopo = actionInfo.price_after || actionInfo.prezzo_dopo || 108;
            const percentuale = actionInfo.sconto_percent || actionInfo.percentuale || -10;

            // Toast con undo
            ActionTracking.showActionToast({
                type: 'success',
                message: `Prezzi aggiornati per ${notti} notti`,
                detail: `€${prezzoPrima} → €${prezzoDopo} (${percentuale >= 0 ? '+' : ''}${percentuale}%)`,
                undoCallback: () => undoSuggestion(id),
                undoTimeout: 10000,
                viewDetailsCallback: () => showActionSummary(actionInfo, applicationId)
            });

            // Summary panel con application_id per link monitoring
            showActionSummary(actionInfo, applicationId);
        } else {
            // Fallback al toast semplice
            showToast('Suggerimento applicato con successo!', 'success');
        }

        // Reload data dopo breve delay (per permettere undo)
        setTimeout(() => loadData(), 500);

    } catch (error) {
        console.error('Error applying suggestion:', error);
        if (window.ActionTracking) {
            ActionTracking.showActionToast({
                type: 'error',
                message: 'Errore applicazione suggerimento',
                detail: error.message || 'Riprova più tardi',
                undoTimeout: 5000
            });
        } else {
            showToast(error.message || 'Errore durante applicazione suggerimento', 'error');
        }
    }
}

// Undo suggestion
async function undoSuggestion(id) {
    try {
        if (DEBUG_REVENUE) console.log('Undoing suggestion:', id);

        const response = await fetch(`${API_BASE}/suggestions/${id}/action?hotel_code=${hotelCode}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                action: 'undo'
            })
        });

        if (!response.ok) {
            throw new Error('Errore durante annullamento');
        }

        // Reload data
        loadData();

    } catch (error) {
        console.error('Error undoing suggestion:', error);
        if (window.Toast) {
            Toast.error('Impossibile annullare: ' + error.message);
        }
    }
}

// Show action summary panel dopo applicazione suggerimento
function showActionSummary(actionInfo, applicationId = null) {
    if (!window.ActionTracking) {
        console.warn('ActionTracking non disponibile');
        return;
    }

    const {
        camera = 'Standard Double',
        periodo = '15 Gen - 31 Gen',
        notti = 17,
        dates_updated = notti,
        prezzo_prima = 120,
        price_before = prezzo_prima,
        prezzo_dopo = 108,
        price_after = prezzo_dopo,
        percentuale = -10,
        sconto_percent = percentuale,
        revenue_stimato = 1836
    } = actionInfo;

    // Genera URL monitoring se abbiamo application_id
    const monitoringUrl = applicationId ? `monitoring.html?application_id=${applicationId}` : null;

    ActionTracking.showSummaryPanel({
        camera,
        periodo,
        notti: dates_updated || notti,
        prezzoPrima: price_before || prezzo_prima,
        prezzoDopo: price_after || prezzo_dopo,
        percentuale: sconto_percent || percentuale,
        revenueStimato: revenue_stimato,
        monitoringUrl
    });
}

// ============================================
// AI HEALTH & PERFORMANCE ALERTS
// ============================================

// Fetch AI health metrics
async function fetchAIHealth() {
    try {
        const response = await fetch(
            `/api/pricing/ai-health?hotel_code=${hotelCode}&days=30`
        );

        if (!response.ok) {
            return null;
        }

        const data = await response.json();
        if (DEBUG_REVENUE) console.log("[AIHealth] API response:", data);
        return data;
    } catch (error) {
        return null;
    }
}

// Check and show performance alerts
function checkPerformanceAlerts(aiHealth) {
    if (!aiHealth) return;

    const perf = aiHealth.performance || {};
    const warningRate = perf.warning_rate || 0;
    const failureRate = perf.failure_rate || 0;
    const pendingEvals = perf.pending_evaluations || 0;
    const status = aiHealth.status;

    // Alert critico: FAILURE rate alto
    if (failureRate >= 20) {
        showToast(
            `Attenzione: ${failureRate.toFixed(0)}% dei suggerimenti AI ha performance negativa. Verifica la strategia pricing.`,
            'error'
        );
        return;
    }

    // Alert warning: WARNING rate alto
    if (warningRate >= 30) {
        showToast(
            `${warningRate.toFixed(0)}% dei suggerimenti sotto le attese. Considera di rivedere i parametri.`,
            'warning'
        );
        return;
    }

    // Alert status generale
    if (status === 'NEEDS_IMPROVEMENT') {
        showToast(
            'AI performance da migliorare. Acceptance rate basso o risultati sotto attese.',
            'warning'
        );
        return;
    }

    // Info: valutazioni in corso
    if (pendingEvals >= 5) {
        // Non mostrare toast per pending - solo info in console
        console.debug(`${pendingEvals} valutazioni AI in corso`);
    }
}

// ============================================
// INIT - Deve essere caricato per ultimo
// ============================================

document.addEventListener('DOMContentLoaded', () => {

    // Hotel selector change handler
    const hotelSelect = document.getElementById('hotelSelect');
    if (hotelSelect) {
        hotelSelect.addEventListener('change', function() {
            hotelCode = this.value;
            if (DEBUG_REVENUE) console.log('Hotel changed to:', hotelCode);
            loadData();
        });
    }

    loadData();

    // Auto refresh ogni 5 min
    refreshIntervalId = setInterval(loadData, 300000);

    // Cleanup interval on page unload
    window.addEventListener('beforeunload', () => {
        if (refreshIntervalId) {
            clearInterval(refreshIntervalId);
        }
    });
});
