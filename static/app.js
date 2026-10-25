/**
 * AI University Helpdesk Chatbot — Final Year B.Tech Engineering Project
 * Client Application Controller:
 * Handles Conversational Chat, Speech-to-Text, Voice Narration,
 * Model Evaluation Sandbox, and Transcript Export.
 */

// Application State
const state = {
    sessionId: "btech_" + Math.random().toString(36).substring(2, 9),
    isTtsEnabled: false,
    isRecording: false,
    activeTab: "chat-tab",
    chatHistory: []
};

// DOM Selectors
const elements = {
    chatMessages: document.getElementById("chatMessages"),
    chatForm: document.getElementById("chatForm"),
    queryInput: document.getElementById("queryInput"),
    typingIndicator: document.getElementById("typingIndicator"),
    voiceInputBtn: document.getElementById("voiceInputBtn"),
    ttsToggleBtn: document.getElementById("ttsToggleBtn"),
    themeToggleBtn: document.getElementById("themeToggleBtn"),
    activeSessionId: document.getElementById("activeSessionId"),
    liveLatency: document.getElementById("liveLatency"),
    clearChatBtn: document.getElementById("clearChatBtn"),
    exportChatBtn: document.getElementById("exportChatBtn"),
    toast: document.getElementById("toast"),
    sandboxQuery: document.getElementById("sandboxQuery"),
    runSandboxBtn: document.getElementById("runSandboxBtn"),
    sandboxResults: document.getElementById("sandboxResults")
};

// ==========================================================================
// Initialization
// ==========================================================================

document.addEventListener("DOMContentLoaded", () => {
    initSession();
    initTheme();
    initTabNavigation();
    initChatHandlers();
    initSpeechRecognition();
    initSandbox();
});

function initSession() {
    if (elements.activeSessionId) {
        elements.activeSessionId.textContent = state.sessionId;
    }
}

// ==========================================================================
// Theme Management (Dark / Light)
// ==========================================================================

function initTheme() {
    const savedTheme = localStorage.getItem("btech_bot_theme") || "dark";
    setTheme(savedTheme);

    if (elements.themeToggleBtn) {
        elements.themeToggleBtn.addEventListener("click", () => {
            const newTheme = document.body.classList.contains("theme-light") ? "dark" : "light";
            setTheme(newTheme);
        });
    }
}

function setTheme(theme) {
    if (theme === "light") {
        document.body.classList.remove("theme-dark");
        document.body.classList.add("theme-light");
        if (elements.themeToggleBtn) elements.themeToggleBtn.innerHTML = '<i class="fa-solid fa-moon"></i>';
        localStorage.setItem("btech_bot_theme", "light");
    } else {
        document.body.classList.remove("theme-light");
        document.body.classList.add("theme-dark");
        if (elements.themeToggleBtn) elements.themeToggleBtn.innerHTML = '<i class="fa-solid fa-sun"></i>';
        localStorage.setItem("btech_bot_theme", "dark");
    }
}

// ==========================================================================
// Tab Navigation (College Viva Sections)
// ==========================================================================

function initTabNavigation() {
    const tabs = document.querySelectorAll(".nav-tab");
    tabs.forEach(tab => {
        tab.addEventListener("click", () => {
            const targetId = tab.getAttribute("data-tab");
            switchTab(targetId);
        });
    });
}

function switchTab(tabId) {
    document.querySelectorAll(".nav-tab").forEach(t => {
        t.classList.toggle("active", t.getAttribute("data-tab") === tabId);
    });

    document.querySelectorAll(".tab-pane").forEach(pane => {
        pane.classList.toggle("active", pane.id === tabId);
    });

    state.activeTab = tabId;
}

// ==========================================================================
// Chat Flow & Real-time AI Querying
// ==========================================================================

function initChatHandlers() {
    if (elements.chatForm) {
        elements.chatForm.addEventListener("submit", (e) => {
            e.preventDefault();
            const text = elements.queryInput.value.trim();
            if (text) {
                sendUserMessage(text);
                elements.queryInput.value = "";
            }
        });
    }

    // Quick chips & prompt suggestions click delegation
    document.addEventListener("click", (e) => {
        const chip = e.target.closest(".chip-btn, .suggestion-pill");
        if (chip) {
            const query = chip.getAttribute("data-query");
            if (query) {
                switchTab("chat-tab");
                sendUserMessage(query);
            }
        }
    });

    // Reset Chat
    if (elements.clearChatBtn) {
        elements.clearChatBtn.addEventListener("click", () => {
            if (confirm("Reset conversation history?")) {
                elements.chatMessages.innerHTML = "";
                state.chatHistory = [];
                showToast("Chat reset.");
            }
        });
    }

    // Export Chat
    if (elements.exportChatBtn) {
        elements.exportChatBtn.addEventListener("click", exportConversation);
    }

    // TTS Toggle Button
    if (elements.ttsToggleBtn) {
        elements.ttsToggleBtn.addEventListener("click", () => {
            state.isTtsEnabled = !state.isTtsEnabled;
            elements.ttsToggleBtn.classList.toggle("active", state.isTtsEnabled);
            elements.ttsToggleBtn.innerHTML = state.isTtsEnabled 
                ? '<i class="fa-solid fa-volume-high" style="color: var(--accent-emerald);"></i>' 
                : '<i class="fa-solid fa-volume-xmark"></i>';
            showToast(state.isTtsEnabled ? "Voice narration active." : "Voice narration muted.");
        });
    }
}

async function sendUserMessage(query) {
    appendUserBubble(query);

    if (elements.typingIndicator) elements.typingIndicator.style.display = "flex";
    elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;

    const startTime = performance.now();

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                query: query,
                session_id: state.sessionId
            })
        });

        const data = await response.json();
        const latency = Math.round(performance.now() - startTime);

        if (elements.liveLatency) {
            elements.liveLatency.textContent = `${latency} ms`;
        }

        if (elements.typingIndicator) elements.typingIndicator.style.display = "none";
        appendAssistantBubble(data);

        if (state.isTtsEnabled) {
            speakText(data.reply);
        }

    } catch (err) {
        if (elements.typingIndicator) elements.typingIndicator.style.display = "none";
        appendAssistantBubble({
            reply: "Server communication error. Please ensure python server.py is running on port 8000.",
            intent: "error",
            confidence: 0,
            category: "System",
            suggestions: ["Check connection", "Retry query"]
        });
    }
}

function appendUserBubble(text) {
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const msgDiv = document.createElement("div");
    msgDiv.className = "message user-message";
    msgDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fa-solid fa-user-graduate"></i>
        </div>
        <div class="message-body">
            <div class="message-header">
                <span class="sender-name">Student</span>
                <span class="message-time">${time}</span>
            </div>
            <div class="message-text">${escapeHtml(text)}</div>
        </div>
    `;
    elements.chatMessages.appendChild(msgDiv);
    elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;

    state.chatHistory.push({ role: "Student", text: text, time: time });
}

function appendAssistantBubble(data) {
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const msgDiv = document.createElement("div");
    msgDiv.className = "message assistant-message";

    const confPercent = Math.round((data.confidence || 0.95) * 100);
    const confClass = confPercent >= 80 ? "confidence-high" : "confidence-med";

    const formattedHtml = formatMarkdown(data.reply);

    let suggHtml = "";
    if (data.suggestions && data.suggestions.length > 0) {
        suggHtml = `
            <div class="message-suggestions">
                <span class="sugg-label"><i class="fa-regular fa-lightbulb"></i> Related Topics:</span>
                ${data.suggestions.map(s => `<button class="suggestion-pill" data-query="${escapeHtml(s)}">${escapeHtml(s)}</button>`).join("")}
            </div>
        `;
    }

    msgDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fa-solid fa-robot"></i>
        </div>
        <div class="message-body">
            <div class="message-header">
                <span class="sender-name">University AI Assistant</span>
                <span class="meta-tag intent">Intent: ${escapeHtml(data.intent || "general")}</span>
                <span class="meta-tag ${confClass}">${confPercent}% Confidence</span>
                <span class="message-time">${time}</span>
            </div>
            <div class="message-text">${formattedHtml}</div>
            ${suggHtml}
            <div class="message-actions">
                <button class="action-btn" onclick="copyMessage(this)" title="Copy text">
                    <i class="fa-regular fa-copy"></i> Copy
                </button>
                <button class="action-btn" onclick="submitFeedback(this, '${escapeHtml(data.intent)}', 1)" title="Helpful answer">
                    <i class="fa-regular fa-thumbs-up"></i> Helpful
                </button>
                <button class="action-btn" onclick="submitFeedback(this, '${escapeHtml(data.intent)}', -1)" title="Needs improvement">
                    <i class="fa-regular fa-thumbs-down"></i>
                </button>
            </div>
        </div>
    `;

    elements.chatMessages.appendChild(msgDiv);
    elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;

    state.chatHistory.push({ role: "AI Assistant", text: data.reply, intent: data.intent, time: time });
}

function formatMarkdown(text) {
    if (!text) return "";
    let html = escapeHtml(text);
    html = html.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
    html = html.replace(/\n- (.*?)(?=\n|$)/g, "<li>$1</li>");
    html = html.replace(/(<li>.*<\/li>)/gs, "<ul>$1</ul>");
    html = html.replace(/\n\n/g, "<br><br>");
    html = html.replace(/\n/g, "<br>");
    return html;
}

function escapeHtml(string) {
    return String(string)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function copyMessage(btn) {
    const text = btn.closest(".message-body").querySelector(".message-text").innerText;
    navigator.clipboard.writeText(text).then(() => {
        showToast("Answer copied to clipboard!");
    });
}

async function submitFeedback(btn, intent, rating) {
    try {
        const query = state.chatHistory.length > 1 ? state.chatHistory[state.chatHistory.length - 2].text : "query";
        await fetch("/api/feedback", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                session_id: state.sessionId,
                query: query,
                intent: intent,
                rating: rating
            })
        });

        btn.classList.add(rating > 0 ? "active-pos" : "active-neg");
        showToast(rating > 0 ? "Feedback recorded: Helpful!" : "Feedback logged for retraining.");
    } catch (e) {
        showToast("Feedback recorded.");
    }
}

function exportConversation() {
    if (state.chatHistory.length === 0) {
        showToast("No chat history to export.");
        return;
    }

    let textContent = `=======================================================\n`;
    textContent += `AI UNIVERSITY HELPDESK CHATBOT — VIVA TEST TRANSCRIPT\n`;
    textContent += `Session: ${state.sessionId} | Generated: ${new Date().toLocaleString()}\n`;
    textContent += `=======================================================\n\n`;

    state.chatHistory.forEach(item => {
        textContent += `[${item.time}] ${item.role.toUpperCase()}:\n${item.text}\n\n`;
    });

    const blob = new Blob([textContent], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `btech_chatbot_transcript_${state.sessionId}.txt`;
    link.click();
    URL.revokeObjectURL(url);
    showToast("Transcript downloaded.");
}

// ==========================================================================
// Speech Recognition (STT) & Speech Synthesis (TTS)
// ==========================================================================

function initSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        if (elements.voiceInputBtn) elements.voiceInputBtn.style.display = "none";
        return;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.lang = "en-US";
    recognition.interimResults = false;

    if (elements.voiceInputBtn) {
        elements.voiceInputBtn.addEventListener("click", () => {
            if (!state.isRecording) {
                recognition.start();
                state.isRecording = true;
                elements.voiceInputBtn.classList.add("recording");
                showToast("Listening... Speak your university query now.");
            } else {
                recognition.stop();
                state.isRecording = false;
                elements.voiceInputBtn.classList.remove("recording");
            }
        });
    }

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        elements.queryInput.value = transcript;
        state.isRecording = false;
        elements.voiceInputBtn.classList.remove("recording");
        sendUserMessage(transcript);
        elements.queryInput.value = "";
    };

    recognition.onerror = () => {
        state.isRecording = false;
        if (elements.voiceInputBtn) elements.voiceInputBtn.classList.remove("recording");
        showToast("Speech recognition stopped.");
    };

    recognition.onend = () => {
        state.isRecording = false;
        if (elements.voiceInputBtn) elements.voiceInputBtn.classList.remove("recording");
    };
}

function speakText(text) {
    if (!('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();
    const clean = text.replace(/[*#-_]/g, " ").replace(/\s+/g, " ");
    const utterance = new SpeechSynthesisUtterance(clean);
    utterance.rate = 1.05;
    window.speechSynthesis.speak(utterance);
}

// ==========================================================================
// Model Testing Sandbox (For Viva Evaluation)
// ==========================================================================

function initSandbox() {
    if (elements.runSandboxBtn) {
        elements.runSandboxBtn.addEventListener("click", () => {
            const query = elements.sandboxQuery.value.trim();
            if (query) {
                runSandboxDiagnostic(query);
            }
        });
    }

    if (elements.sandboxQuery) {
        runSandboxDiagnostic(elements.sandboxQuery.value);
    }
}

async function runSandboxDiagnostic(query) {
    try {
        const res = await fetch("/api/sandbox", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query: query })
        });
        const data = await res.json();

        document.getElementById("sbTopIntent").textContent = data.top_intent;
        document.getElementById("sbCategory").textContent = `Category: ${data.category}`;
        document.getElementById("sbConfidence").textContent = `${Math.round(data.confidence * 100)}%`;

        const list = document.getElementById("sbProgressList");
        list.innerHTML = "";

        (data.ranked_predictions || []).slice(0, 6).forEach(item => {
            const pct = Math.round(item.score * 100);
            const div = document.createElement("div");
            div.className = "intent-bar-row";
            div.innerHTML = `
                <div class="bar-meta">
                    <span>${escapeHtml(item.intent)}</span>
                    <strong>${pct}%</strong>
                </div>
                <div class="bar-track">
                    <div class="bar-fill" style="width: ${pct}%;"></div>
                </div>
            `;
            list.appendChild(div);
        });

    } catch (e) {
        console.error("Sandbox evaluation error", e);
    }
}

// ==========================================================================
// Toast Notifications
// ==========================================================================

function showToast(message) {
    if (!elements.toast) return;
    elements.toast.textContent = message;
    elements.toast.classList.add("show");
    setTimeout(() => {
        elements.toast.classList.remove("show");
    }, 2600);
}
