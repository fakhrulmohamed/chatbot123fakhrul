/**
 * CampusAssist College FAQ Chatbot Frontend Logic
 */

document.addEventListener("DOMContentLoaded", () => {
  // Elements
  const chatMessages = document.getElementById("chat-messages");
  const chatForm = document.getElementById("chat-form");
  const userInput = document.getElementById("user-input");
  const typingIndicator = document.getElementById("typing-indicator");
  const voiceBtn = document.getElementById("voice-btn");
  const clearChatBtn = document.getElementById("clear-chat-btn");
  const themeToggle = document.getElementById("theme-toggle");
  const sunIcon = document.getElementById("sun-icon");
  const moonIcon = document.getElementById("moon-icon");

  const tabBtns = document.querySelectorAll(".tab-btn");
  const viewPanels = document.querySelectorAll(".view-panel");

  const directoryCategories = document.getElementById("directory-categories");
  const faqAccordionList = document.getElementById("faq-accordion-list");
  const faqSearchInput = document.getElementById("faq-search-input");

  let allFaqsCache = [];
  let currentCategory = "all";

  // --- 1. Theme Toggle (Dark/Light) ---
  const savedTheme = localStorage.getItem("campus_theme") || "light-theme";
  document.body.className = savedTheme;
  updateThemeIcons(savedTheme);

  themeToggle.addEventListener("click", () => {
    const isDark = document.body.classList.contains("dark-theme");
    const newTheme = isDark ? "light-theme" : "dark-theme";
    document.body.className = newTheme;
    localStorage.setItem("campus_theme", newTheme);
    updateThemeIcons(newTheme);
  });

  function updateThemeIcons(theme) {
    if (theme === "dark-theme") {
      sunIcon.classList.remove("hidden");
      moonIcon.classList.add("hidden");
    } else {
      sunIcon.classList.add("hidden");
      moonIcon.classList.remove("hidden");
    }
  }

  // --- 2. Tab Navigation ---
  tabBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      tabBtns.forEach(b => b.classList.remove("active"));
      viewPanels.forEach(p => p.classList.remove("active"));

      btn.classList.add("active");
      const targetId = btn.getAttribute("data-tab");
      document.getElementById(targetId).classList.add("active");

      if (targetId === "directory-view" && allFaqsCache.length === 0) {
        loadFaqDirectory();
      }
    });
  });

  // --- 3. Chat Mechanics ---
  function getTimeString() {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }

  function appendUserMessage(text) {
    const msgDiv = document.createElement("div");
    msgDiv.className = "message user-message";
    msgDiv.innerHTML = `
      <div class="avatar user-avatar">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
          <circle cx="12" cy="7" r="4"></circle>
        </svg>
      </div>
      <div class="bubble">
        <div class="bubble-header">
          <span class="bubble-time">${getTimeString()}</span>
        </div>
        <div class="bubble-body">${escapeHTML(text)}</div>
      </div>
    `;
    chatMessages.appendChild(msgDiv);
    scrollToBottom();
  }

  function appendBotMessage(data) {
    const msgDiv = document.createElement("div");
    msgDiv.className = "message bot-message";

    const categoryBadge = data.category ? `<span class="badge-tag">${data.category}</span>` : "";
    const faqId = data.faq_id || "";

    // Generate links if present
    let linksHtml = "";
    if (data.quick_links && data.quick_links.length > 0) {
      linksHtml = `<div class="bubble-links">` + data.quick_links.map(l => 
        `<a href="${l.url}" class="resource-link" target="_blank">🔗 ${l.label}</a>`
      ).join("") + `</div>`;
    }

    // Generate suggestions if present
    let suggestionsHtml = "";
    if (data.suggestions && data.suggestions.length > 0) {
      suggestionsHtml = `
        <div class="quick-suggestions-box">
          <div class="suggestions-title">💡 You might also want to ask:</div>
          <div class="suggestions-list">
            ${data.suggestions.map(s => `<button class="suggestion-chip">${s}</button>`).join("")}
          </div>
        </div>
      `;
    }

    msgDiv.innerHTML = `
      <div class="avatar bot-avatar">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M22 10v6M2 10l10-5 10 5-10 5z"/>
          <path d="M6 12v5c3 3 9 3 12 0v-5"/>
        </svg>
      </div>
      <div class="bubble">
        <div class="bubble-header">
          <span class="bot-name">CampusAssist Bot</span>
          ${categoryBadge}
          <span class="bubble-time">${getTimeString()}</span>
        </div>
        <div class="bubble-body">
          ${data.answer}
          ${linksHtml}
        </div>
        ${suggestionsHtml}
        <div class="bubble-footer">
          <span>Was this helpful?</span>
          <div class="bubble-actions">
            <button class="mini-action-btn speak-btn" title="Listen to response">
              🔊 Read
            </button>
            <button class="mini-action-btn feedback-btn" data-faq="${faqId}" data-val="yes" title="Helpful">
              👍 Yes
            </button>
            <button class="mini-action-btn feedback-btn" data-faq="${faqId}" data-val="no" title="Not helpful">
              👎 No
            </button>
          </div>
        </div>
      </div>
    `;

    chatMessages.appendChild(msgDiv);
    scrollToBottom();

    // Attach speech listener
    const speakBtn = msgDiv.querySelector(".speak-btn");
    speakBtn.addEventListener("click", () => {
      speakText(msgDiv.querySelector(".bubble-body").innerText);
    });

    // Attach feedback listener
    const feedbackBtns = msgDiv.querySelectorAll(".feedback-btn");
    feedbackBtns.forEach(btn => {
      btn.addEventListener("click", () => {
        const val = btn.getAttribute("data-val") === "yes";
        feedbackBtns.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        sendFeedback(faqId, val);
      });
    });
  }

  function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function escapeHTML(str) {
    return str.replace(/[&<>'"]/g, 
      tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag)
    );
  }

  async function handleSendMessage(queryText) {
    const text = (queryText || userInput.value).trim();
    if (!text) return;

    appendUserMessage(text);
    userInput.value = "";
    showTyping(true);

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text })
      });
      const data = await res.json();
      setTimeout(() => {
        showTyping(false);
        appendBotMessage(data);
      }, 400); // realistic typing pause
    } catch (err) {
      showTyping(false);
      appendBotMessage({
        answer: "Sorry, I am having trouble reaching the college database server right now. Please try again shortly or contact admissions@college.edu.",
        suggestions: ["Admissions helpline contact details"]
      });
    }
  }

  function showTyping(show) {
    if (show) {
      typingIndicator.classList.remove("hidden");
      scrollToBottom();
    } else {
      typingIndicator.classList.add("hidden");
    }
  }

  chatForm.addEventListener("submit", (e) => {
    e.preventDefault();
    handleSendMessage();
  });

  // Handle clicking on suggestions or topic chips
  document.addEventListener("click", (e) => {
    if (e.target.classList.contains("suggestion-chip")) {
      handleSendMessage(e.target.innerText.trim());
    } else if (e.target.classList.contains("topic-chip")) {
      const q = e.target.getAttribute("data-query");
      handleSendMessage(q);
    }
  });

  // --- 4. Text-to-Speech (TTS) ---
  function speakText(text) {
    if (!('speechSynthesis' in window)) {
      alert("Text-to-speech is not supported in this browser.");
      return;
    }
    window.speechSynthesis.cancel();
    const clean = text.replace(/<[^>]*>?/gm, '').replace(/https?:\/\/\S+/g, '');
    const utterance = new SpeechSynthesisUtterance(clean);
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    window.speechSynthesis.speak(utterance);
  }

  // --- 5. Voice Input (Speech-to-Text) ---
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (SpeechRecognition) {
    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.lang = 'en-US';

    recognition.onstart = () => {
      voiceBtn.classList.add("listening");
      userInput.placeholder = "Listening... Speak your college question";
    };

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      userInput.value = transcript;
      handleSendMessage(transcript);
    };

    recognition.onerror = () => {
      voiceBtn.classList.remove("listening");
      userInput.placeholder = "Ask about admissions, fees, hostel, placements, exams...";
    };

    recognition.onend = () => {
      voiceBtn.classList.remove("listening");
      userInput.placeholder = "Ask about admissions, fees, hostel, placements, exams...";
    };

    voiceBtn.addEventListener("click", () => {
      if (voiceBtn.classList.contains("listening")) {
        recognition.stop();
      } else {
        recognition.start();
      }
    });
  } else {
    voiceBtn.style.display = "none";
  }

  // --- 6. Clear Chat ---
  clearChatBtn.addEventListener("click", () => {
    if (confirm("Clear current conversation history?")) {
      chatMessages.innerHTML = `
        <div class="message bot-message">
          <div class="avatar bot-avatar">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M22 10v6M2 10l10-5 10 5-10 5z"/>
              <path d="M6 12v5c3 3 9 3 12 0v-5"/>
            </svg>
          </div>
          <div class="bubble">
            <div class="bubble-header">
              <span class="bot-name">CampusAssist Bot</span>
              <span class="bubble-time">${getTimeString()}</span>
            </div>
            <div class="bubble-body">
              <p>Chat cleared! What college query can I help you explore?</p>
            </div>
            <div class="quick-suggestions-box">
              <div class="suggestions-list">
                <button class="suggestion-chip">How do I apply for admission?</button>
                <button class="suggestion-chip">What is the fee structure for various programs?</button>
                <button class="suggestion-chip">What are the placement statistics?</button>
              </div>
            </div>
          </div>
        </div>
      `;
    }
  });

  // --- 7. Feedback API ---
  async function sendFeedback(faqId, helpful) {
    try {
      await fetch("/api/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ faq_id: faqId, helpful: helpful })
      });
    } catch (e) {
      console.error("Feedback failed", e);
    }
  }

  // --- 8. FAQ Knowledge Base Directory ---
  async function loadFaqDirectory() {
    try {
      const [faqRes, catRes] = await Promise.all([
        fetch("/api/faqs"),
        fetch("/api/categories")
      ]);
      const faqData = await faqRes.json();
      const catData = await catRes.json();

      allFaqsCache = faqData.faqs || [];
      renderCategoryFilters(catData.categories || []);
      renderAccordionList(allFaqsCache);
    } catch (err) {
      faqAccordionList.innerHTML = `<div class="error-msg">Failed to load FAQs. Please refresh.</div>`;
    }
  }

  function renderCategoryFilters(categories) {
    directoryCategories.innerHTML = `<button class="filter-chip active" data-cat="all">All FAQs (${allFaqsCache.length})</button>`;
    categories.forEach(cat => {
      const count = allFaqsCache.filter(f => f.category === cat).length;
      const chip = document.createElement("button");
      chip.className = "filter-chip";
      chip.setAttribute("data-cat", cat);
      chip.innerText = `${cat} (${count})`;
      chip.addEventListener("click", () => {
        document.querySelectorAll(".filter-chip").forEach(c => c.classList.remove("active"));
        chip.classList.add("active");
        currentCategory = cat;
        filterAndRenderFaqs();
      });
      directoryCategories.appendChild(chip);
    });

    directoryCategories.querySelector('[data-cat="all"]').addEventListener("click", function() {
      document.querySelectorAll(".filter-chip").forEach(c => c.classList.remove("active"));
      this.classList.add("active");
      currentCategory = "all";
      filterAndRenderFaqs();
    });
  }

  function filterAndRenderFaqs() {
    const searchTerm = faqSearchInput.value.toLowerCase().trim();
    let filtered = allFaqsCache;

    if (currentCategory !== "all") {
      filtered = filtered.filter(f => f.category === currentCategory);
    }

    if (searchTerm) {
      filtered = filtered.filter(f => 
        f.question.toLowerCase().includes(searchTerm) ||
        f.answer.toLowerCase().includes(searchTerm) ||
        (f.keywords && f.keywords.some(k => k.toLowerCase().includes(searchTerm)))
      );
    }

    renderAccordionList(filtered);
  }

  faqSearchInput.addEventListener("input", filterAndRenderFaqs);

  function renderAccordionList(faqs) {
    if (faqs.length === 0) {
      faqAccordionList.innerHTML = `<div class="empty-notice" style="text-align:center; padding:30px; color:var(--text-muted);">No matching FAQs found for your search. Try different keywords.</div>`;
      return;
    }

    faqAccordionList.innerHTML = faqs.map(f => `
      <div class="accordion-item" id="${f.id}">
        <div class="accordion-header">
          <div class="accordion-title-wrap">
            <span class="accordion-category-badge">${f.category}</span>
            <span class="accordion-title">${f.question}</span>
          </div>
          <svg class="accordion-arrow" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="6 9 12 15 18 9"></polyline>
          </svg>
        </div>
        <div class="accordion-body">
          <div class="faq-content">${f.answer}</div>
          ${f.quick_links && f.quick_links.length > 0 ? `
            <div class="bubble-links" style="margin-top:12px;">
              ${f.quick_links.map(l => `<a href="${l.url}" class="resource-link">🔗 ${l.label}</a>`).join("")}
            </div>` : ''}
          <div style="margin-top:14px; display:flex; gap:10px;">
            <button class="topic-chip ask-this-btn" data-q="${f.question}">Ask this in Chat &rarr;</button>
          </div>
        </div>
      </div>
    `).join("");

    // Accordion toggle click handlers
    faqAccordionList.querySelectorAll(".accordion-header").forEach(header => {
      header.addEventListener("click", () => {
        const item = header.parentElement;
        const isOpen = item.classList.contains("open");
        faqAccordionList.querySelectorAll(".accordion-item").forEach(i => i.classList.remove("open"));
        if (!isOpen) {
          item.classList.add("open");
        }
      });
    });

    // "Ask this in Chat" button inside accordion card
    faqAccordionList.querySelectorAll(".ask-this-btn").forEach(btn => {
      btn.addEventListener("click", (e) => {
        e.stopPropagation();
        const q = btn.getAttribute("data-q");
        // Switch to chat tab
        document.querySelector('[data-tab="chat-view"]').click();
        handleSendMessage(q);
      });
    });
  }

  // Preload FAQs when idle
  setTimeout(loadFaqDirectory, 1000);
});
