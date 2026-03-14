// SPDX-License-Identifier: Apache-2.0
// Copyright 2026 CervellaSwarm Contributors

/**
 * Tour UI logic for A Tour of Lingua Universale.
 *
 * Depends on:
 *   - window.LU_TOUR (from tour.js)
 *   - window.LU_TOUR_VERSION (from tour.js)
 *   - state.editor (Monaco editor instance from index.html)
 *   - dom.* (DOM references from index.html)
 *   - escHtml() (from index.html)
 *   - clearOutput() (from index.html)
 *   - handleCheck(), handleRun() (from index.html)
 */

/* global state, dom, escHtml, clearOutput */

// ============================================================
// TOUR STATE
// ============================================================

const tourState = {
  active: false,
  currentStep: 0,
  progress: {},           // { stepId: true }
  savedEditorContent: "", // editor content before entering tour
  savedExampleId: "",     // example ID before entering tour
  version: 0,            // for invalidating stale progress
};

// ============================================================
// HELPERS
// ============================================================

// Uses $() from index.html: const $ = (id) => document.getElementById(id);

/** Flatten all steps from chapters into a single ordered array. */
function getTourSteps() {
  const steps = [];
  window.LU_TOUR.chapters.forEach(function (ch) {
    ch.steps.forEach(function (step) {
      steps.push(Object.assign({}, step, {
        chapterId: ch.id,
        chapterTitle: ch.title,
      }));
    });
  });
  return steps;
}

// ============================================================
// PERSISTENCE (localStorage)
// ============================================================

function loadTourProgress() {
  try {
    var savedVersion = parseInt(localStorage.getItem("lu-tour-version") || "0", 10);
    if (savedVersion !== window.LU_TOUR_VERSION) {
      // Tour content changed; reset progress
      localStorage.removeItem("lu-tour-progress");
      localStorage.removeItem("lu-tour-step");
      localStorage.setItem("lu-tour-version", String(window.LU_TOUR_VERSION));
      tourState.progress = {};
      tourState.currentStep = 0;
      return;
    }
    var saved = localStorage.getItem("lu-tour-progress");
    if (saved) tourState.progress = JSON.parse(saved);
    var savedStep = localStorage.getItem("lu-tour-step");
    if (savedStep !== null) tourState.currentStep = parseInt(savedStep, 10) || 0;
  } catch (_) {
    tourState.progress = {};
  }
}

function saveTourProgress() {
  try {
    localStorage.setItem("lu-tour-progress", JSON.stringify(tourState.progress));
    localStorage.setItem("lu-tour-step", String(tourState.currentStep));
    localStorage.setItem("lu-tour-version", String(window.LU_TOUR_VERSION));
  } catch (_) {
    // localStorage full or unavailable
  }
}

// ============================================================
// COMPLETION TRACKING
// ============================================================

/**
 * Mark the current tour step as completed (Check/Run succeeded).
 * Called from index.html after successful output in tour mode.
 */
function markTourStepCompleted() {
  var steps = getTourSteps();
  var step = steps[tourState.currentStep];
  if (!step) return;
  tourState.progress[step.id] = "done";
  saveTourProgress();

  // Celebration on the very last step
  if (tourState.currentStep === steps.length - 1) {
    var resultEl = $("tour-result");
    if (resultEl && !resultEl.querySelector(".tour-celebration")) {
      var cel = document.createElement("div");
      cel.className = "tour-celebration";
      cel.innerHTML =
        '<strong>You completed the Tour of Lingua Universale!</strong><br>' +
        'Install: <code>pip install cervellaswarm-lingua-universale</code><br>' +
        '<a href="https://lu-debugger.fly.dev/" target="_blank">Watch AI agents live</a> | ' +
        '<a href="https://pypi.org/project/cervellaswarm-lingua-universale/" target="_blank">PyPI</a>';
      resultEl.appendChild(cel);
    }
  }
}

// Expose for index.html
window.markTourStepCompleted = markTourStepCompleted;

// ============================================================
// LIGHTWEIGHT MARKDOWN RENDERER
// ============================================================

/** Sanitize then parse inline markdown (bold, italic, code). */
function inlineMarkdown(text) {
  // escHtml first (F3 Guardiana: prevent XSS)
  var safe = escHtml(text);
  return safe
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/\*([^*]+)\*/g, "<em>$1</em>");
}

/** Render a subset of markdown: paragraphs, bold, italic, code, lists. */
function renderMarkdownLight(text) {
  if (!text) return "";
  return text
    .split("\n\n")
    .map(function (block) {
      block = block.trim();
      if (!block) return "";
      // Unordered list (lines starting with - )
      if (/^[-*]\s/.test(block)) {
        var items = block.split("\n").map(function (line) {
          return "<li>" + inlineMarkdown(line.replace(/^[-*]\s+/, "")) + "</li>";
        }).join("");
        return "<ul>" + items + "</ul>";
      }
      return "<p>" + inlineMarkdown(block) + "</p>";
    })
    .join("");
}

// ============================================================
// ENTER / EXIT TOUR
// ============================================================

function enterTour(startStep) {
  tourState.active = true;
  tourState.savedEditorContent = state.editor.getValue();
  tourState.savedExampleId = state.currentExample || "";

  loadTourProgress();
  if (startStep !== undefined) {
    tourState.currentStep = startStep;
  }

  // Clamp to valid range
  var steps = getTourSteps();
  if (tourState.currentStep >= steps.length) tourState.currentStep = 0;

  // Show tour UI
  $("tour-bar").style.display = "";
  $("tour-panel").style.display = "";
  $("output-area").style.display = "none";
  $("output-empty").style.display = "none";

  // Hide example selector
  var exLabel = document.querySelector(".examples-label");
  if (exLabel) exLabel.style.display = "none";
  dom.exampleSelect.style.display = "none";

  // Update output pane label
  var paneLabel = document.querySelector("#output-pane .pane-label");
  if (paneLabel) {
    paneLabel.dataset.originalLabel = paneLabel.textContent;
    // Find text node and replace
    var nodes = paneLabel.childNodes;
    for (var i = nodes.length - 1; i >= 0; i--) {
      if (nodes[i].nodeType === 3) { nodes[i].textContent = " Tour"; break; }
    }
  }

  // Update tour button state
  $("btn-tour").classList.add("active");
  var btnText = $("btn-tour").querySelector(".btn-tour-text");
  if (btnText) btnText.textContent = "Exit Tour";

  renderTourStep();
}

function exitTour() {
  tourState.active = false;
  saveTourProgress();

  // Hide tour UI
  $("tour-bar").style.display = "none";
  $("tour-panel").style.display = "none";
  $("output-area").style.display = "";

  // Show example selector
  var exLabel = document.querySelector(".examples-label");
  if (exLabel) exLabel.style.display = "";
  dom.exampleSelect.style.display = "";

  // Restore output pane label
  var paneLabel = document.querySelector("#output-pane .pane-label");
  if (paneLabel && paneLabel.dataset.originalLabel) {
    var nodes = paneLabel.childNodes;
    for (var i = nodes.length - 1; i >= 0; i--) {
      if (nodes[i].nodeType === 3) { nodes[i].textContent = " Output"; break; }
    }
  }

  // Restore editor content
  state.editor.setValue(tourState.savedEditorContent);
  clearOutput();

  // Update tour button state
  $("btn-tour").classList.remove("active");
  var btnText = $("btn-tour").querySelector(".btn-tour-text");
  if (btnText) {
    var hasProgress = Object.keys(tourState.progress).length > 0;
    btnText.textContent = hasProgress ? "Resume Tour" : "Tour";
  }

  // Remove suggested button highlights
  dom.btnCheck.classList.remove("suggested-btn");
  dom.btnRun.classList.remove("suggested-btn");
}

// ============================================================
// RENDER TOUR STEP
// ============================================================

function renderTourStep() {
  var steps = getTourSteps();
  var step = steps[tourState.currentStep];
  if (!step) return;

  // Update editor
  state.editor.setValue(step.code);
  dom.editorInfo.textContent = "tour/" + step.id + ".lu";

  // Tour panel content
  $("tour-chapter-tag").textContent = step.chapterTitle;
  $("tour-step-title").textContent = step.title;
  $("tour-explanation").innerHTML = renderMarkdownLight(step.explanation);

  // Hint
  var hintEl = $("tour-hint");
  if (step.hint) {
    hintEl.textContent = step.hint;
    hintEl.style.display = "";
  } else {
    hintEl.textContent = "";
    hintEl.style.display = "none";
  }

  // Action prompt
  var actionEl = $("tour-action-prompt");
  dom.btnCheck.classList.remove("suggested-btn");
  dom.btnRun.classList.remove("suggested-btn");

  if (step.suggestedAction === "check") {
    actionEl.innerHTML = '<span>Try it: press <strong>Check</strong> to validate this code.</span>';
    dom.btnCheck.classList.add("suggested-btn");
  } else if (step.suggestedAction === "run") {
    actionEl.innerHTML = '<span>Try it: press <strong>Run</strong> to execute this code.</span>';
    dom.btnRun.classList.add("suggested-btn");
  } else {
    actionEl.innerHTML = "";
  }

  // Exercise controls
  var exerciseEl = $("tour-exercise-controls");
  if (step.isExercise && step.solution) {
    exerciseEl.style.display = "";
  } else {
    exerciseEl.style.display = "none";
  }

  // Clear inline result
  $("tour-result").innerHTML = "";

  // Navigation state
  $("tour-prev").disabled = tourState.currentStep === 0;
  $("tour-next").disabled = tourState.currentStep === steps.length - 1;
  $("tour-position").textContent = (tourState.currentStep + 1) + " / " + steps.length;

  // Progress bar
  var pct = ((tourState.currentStep + 1) / steps.length) * 100;
  $("tour-progress-bar").style.width = pct + "%";

  // Mark visited
  tourState.progress[step.id] = true;
  saveTourProgress();

  // Scroll tour panel to top
  $("tour-panel").scrollTop = 0;
}

// ============================================================
// CHAPTERS OVERLAY
// ============================================================

function renderChaptersOverlay() {
  var listEl = $("tour-chapters-list");
  listEl.innerHTML = "";
  var allSteps = getTourSteps();
  var globalIdx = 0;

  window.LU_TOUR.chapters.forEach(function (ch) {
    var card = document.createElement("div");
    card.className = "tour-chapter-card";

    var title = document.createElement("div");
    title.className = "ch-title";
    title.textContent = ch.title;
    card.appendChild(title);

    var desc = document.createElement("div");
    desc.className = "ch-desc";
    var completed = ch.steps.filter(function (s) { return tourState.progress[s.id] === "done"; }).length;
    desc.textContent = completed + " / " + ch.steps.length + " completed — " + ch.description;
    card.appendChild(desc);

    var dots = document.createElement("div");
    dots.className = "ch-dots";
    var chapterStartIdx = globalIdx;
    ch.steps.forEach(function (s, i) {
      var dot = document.createElement("div");
      dot.className = "ch-dot";
      if (tourState.progress[s.id] === "done") dot.classList.add("completed");
      else if (tourState.progress[s.id]) dot.classList.add("visited");
      if (globalIdx + i === tourState.currentStep) dot.classList.add("current");
      dots.appendChild(dot);
    });
    card.appendChild(dots);

    (function (startIdx) {
      card.addEventListener("click", function () {
        tourState.currentStep = startIdx;
        renderTourStep();
        $("tour-chapters-overlay").style.display = "none";
      });
    })(chapterStartIdx);

    listEl.appendChild(card);
    globalIdx += ch.steps.length;
  });
}

// ============================================================
// EVENT WIRING
// ============================================================

function initTourUI() {
  // Load saved progress to set button text
  loadTourProgress();
  var hasProgress = Object.keys(tourState.progress).length > 0;
  var btnText = $("btn-tour").querySelector(".btn-tour-text");
  if (btnText && hasProgress) {
    btnText.textContent = "Resume Tour";
  }

  // Tour button: toggle tour mode
  $("btn-tour").addEventListener("click", function () {
    if (tourState.active) {
      exitTour();
    } else {
      enterTour();
    }
  });

  // Navigation
  $("tour-prev").addEventListener("click", function () {
    if (tourState.currentStep > 0) {
      tourState.currentStep--;
      renderTourStep();
    }
  });

  $("tour-next").addEventListener("click", function () {
    var steps = getTourSteps();
    if (tourState.currentStep < steps.length - 1) {
      tourState.currentStep++;
      renderTourStep();
    }
  });

  // Chapter overview
  $("tour-chapters-btn").addEventListener("click", function () {
    renderChaptersOverlay();
    $("tour-chapters-overlay").style.display = "flex";
  });

  $("tour-chapters-close").addEventListener("click", function () {
    $("tour-chapters-overlay").style.display = "none";
  });

  // Close chapters overlay on backdrop click
  $("tour-chapters-overlay").addEventListener("click", function (e) {
    if (e.target === $("tour-chapters-overlay")) {
      $("tour-chapters-overlay").style.display = "none";
    }
  });

  // Exit tour button in tour bar
  $("tour-exit").addEventListener("click", function () {
    exitTour();
  });

  // Show solution (exercises)
  $("tour-show-solution").addEventListener("click", function () {
    var steps = getTourSteps();
    var step = steps[tourState.currentStep];
    if (step && step.solution) {
      state.editor.setValue(step.solution);
    }
  });

  // Keyboard shortcuts for tour navigation
  document.addEventListener("keydown", function (e) {
    if (!tourState.active) return;
    // Don't capture if focus is in editor (Monaco handles its own shortcuts)
    if (document.activeElement && document.activeElement.closest("#editor-container")) return;

    if (e.altKey && e.key === "ArrowRight") {
      e.preventDefault();
      $("tour-next").click();
    } else if (e.altKey && e.key === "ArrowLeft") {
      e.preventDefault();
      $("tour-prev").click();
    } else if (e.key === "Escape") {
      exitTour();
    }
  });

  // Check URL hash for #tour auto-entry
  if (window.location.hash === "#tour" ||
      new URLSearchParams(window.location.search).has("tour")) {
    // Wait for Pyodide to be ready, then enter tour
    var waitForReady = setInterval(function () {
      if (state.ready) {
        clearInterval(waitForReady);
        enterTour();
      }
    }, 200);
    // Timeout after 30s
    setTimeout(function () { clearInterval(waitForReady); }, 30000);
  }
}

// ============================================================
// INTEGRATION: redirect renderOutput to tour panel
// ============================================================

/**
 * Called from index.html after tour-ui.js loads.
 * Returns the target element for output rendering.
 */
function getTourOutputTarget() {
  if (tourState.active) {
    return $("tour-result");
  }
  return null; // use default
}

// Export for index.html
window.tourState = tourState;
window.initTourUI = initTourUI;
window.getTourOutputTarget = getTourOutputTarget;
