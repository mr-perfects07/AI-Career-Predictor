const API_BASE = (window.APP_API_BASE_URL || "").replace(/\/$/, "");
const questions = [
  { kicker: "FIRST, THE FUN PART", title: "What kinds of things pull you in?", help: "Pick up to three. Go with what feels interesting, not what sounds impressive.", key: "interests", max: 3, options: [["design", "✳", "Making or designing things"], ["people", "♡", "Understanding and helping people"], ["data", "⌁", "Finding patterns in information"], ["technology", "⌘", "Exploring how technology works"], ["nature", "❋", "Being curious about the natural world"], ["communication", "✎", "Sharing ideas and stories"], ["building", "⌂", "Building something from an idea"], ["learning", "◌", "Learning how people and ideas work"], ["problem solving", "↗", "Untangling tricky problems"]] },
  { kicker: "YOUR NATURAL STRENGTHS", title: "What do people often count on you for?", help: "Choose up to three strengths. You can pick ones you’re still growing, too.", key: "skills", max: 3, options: [["creativity", "✳", "Coming up with fresh ideas"], ["analytical thinking", "⌁", "Spotting patterns and details"], ["communication", "✎", "Explaining things clearly"], ["empathy", "♡", "Noticing how others feel"], ["organization", "▦", "Keeping plans on track"], ["curiosity", "✦", "Asking thoughtful questions"], ["problem solving", "↗", "Finding a way through a challenge"]] },
  { kicker: "SUBJECTS YOU CONNECT WITH", title: "Which subjects feel most like your zone?", help: "Choose up to three. Enjoyment matters more than your grades here.", key: "subjects", max: 3, options: [["mathematics", "∑", "Maths & statistics"], ["computer science", "⌘", "Computing & technology"], ["biology", "❋", "Biology & life sciences"], ["chemistry", "⚗", "Chemistry & materials"], ["art and design", "✳", "Art & design"], ["psychology", "◌", "Psychology & behavior"], ["business", "↗", "Business & entrepreneurship"], ["language and literature", "Aa", "Languages & literature"], ["geography", "⌖", "Geography & environment"], ["economics", "▤", "Economics & society"]] },
  { kicker: "HOW YOU LIKE TO WORK", title: "What kind of workday sounds good?", help: "Pick up to two. There’s no wrong combination.", key: "work", max: 2, options: [["creating", "✳", "Making, designing, or building"], ["research", "⌁", "Investigating and learning"], ["helping others", "♡", "Supporting people directly"], ["collaboration", "◎", "Working through ideas with a team"], ["independent focus", "◌", "Having quiet time to focus"], ["communication", "✎", "Presenting or sharing ideas"], ["problem solving", "↗", "Working out practical challenges"]] },
  { kicker: "WHAT MATTERS TO YOU", title: "What would you like your future work to offer?", help: "Choose up to two priorities. We’ll use these as a gentle nudge in your matches.", key: "priorities", max: 2, options: [["helping others", "♡", "A chance to make a difference"], ["creativity", "✳", "Room to create and experiment"], ["learning", "✦", "New things to learn over time"], ["stability", "▦", "A steady, structured environment"], ["flexibility", "↗", "Variety and room to shape my day"]] }
];

const state = { step: 0, answers: { interests: [], skills: [], subjects: [], work: [], priorities: [] }, results: [], careers: [] };
const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];

async function api(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, { ...options, headers: { "Content-Type": "application/json", ...options.headers } });
  const body = await response.json().catch(() => ({}));
  if (!response.ok) {
    const detail = Array.isArray(body.detail) ? body.detail.map((item) => item.msg).join("; ") : body.detail || "The service returned an error.";
    throw new Error(detail);
  }
  return body;
}

function showView(name) {
  $$(".view").forEach((view) => view.classList.toggle("active", view.id === `${name}-view`));
  $$(".nav-link").forEach((button) => button.classList.toggle("active", button.dataset.view === name));
  window.scrollTo({ top: 0, behavior: "smooth" });
  if (name === "saved") renderSaved();
}
function toast(message) {
  const element = $("#toast"); element.textContent = message; element.classList.add("show");
  clearTimeout(toast.timer); toast.timer = setTimeout(() => element.classList.remove("show"), 3200);
}
function savedIds() {
  try { const ids = JSON.parse(localStorage.getItem("career-predictor-saved") || "[]"); return Array.isArray(ids) ? ids.filter((id) => typeof id === "string") : []; }
  catch { return []; }
}
function setSaved(ids) {
  try { localStorage.setItem("career-predictor-saved", JSON.stringify(ids)); $("#saved-count").textContent = ids.length; }
  catch { toast("Your browser could not save this career."); }
}
function openModal(html) { $("#modal-content").innerHTML = html; $("#modal-backdrop").hidden = false; $("#modal-close").focus(); }
function closeModal() { $("#modal-backdrop").hidden = true; }

function renderQuestion() {
  const question = questions[state.step], percent = Math.round(((state.step + 1) / questions.length) * 100);
  $("#question-count").textContent = `QUESTION ${String(state.step + 1).padStart(2, "0")} / ${String(questions.length).padStart(2, "0")}`;
  $("#progress-label").textContent = `${percent}% complete`; $("#progress-bar").style.width = `${percent}%`;
  $("#question-kicker").textContent = question.kicker; $("#question-title").textContent = question.title; $("#question-help").textContent = question.help;
  $("#prev-button").disabled = state.step === 0;
  $("#next-button").innerHTML = state.step === questions.length - 1 ? "See my matches <span>↗</span>" : "Continue <span>→</span>";
  const options = $("#answer-options"); options.replaceChildren();
  for (const [value, icon, label] of question.options) {
    const selected = state.answers[question.key].includes(value), button = document.createElement("button");
    button.type = "button"; button.className = `answer-card${selected ? " selected" : ""}`; button.setAttribute("aria-pressed", String(selected));
    button.innerHTML = `<span class="answer-icon">${icon}</span><span>${label}</span><span class="answer-check">${selected ? "✓" : ""}</span>`;
    button.addEventListener("click", () => toggleAnswer(question, value)); options.appendChild(button);
  }
  const count = state.answers[question.key].length;
  $("#next-button").disabled = count === 0;
  $("#selection-hint").textContent = count ? `${count} selected${count >= question.max ? " · selection limit reached" : ""}` : "Choose at least one to continue";
}
function toggleAnswer(question, value) {
  const selected = state.answers[question.key], index = selected.indexOf(value);
  if (index >= 0) selected.splice(index, 1);
  else if (selected.length < question.max) selected.push(value);
  else return toast(`Choose up to ${question.max} options`);
  renderQuestion();
}

async function renderResults() {
  const nextButton = $("#next-button"); nextButton.disabled = true; nextButton.textContent = "Finding your matches…";
  try {
    const response = await api("/recommend", { method: "POST", body: JSON.stringify(state.answers) });
    state.results = response.matches; $("#career-results").innerHTML = state.results.map(careerCard).join(""); showView("results");
  } catch (error) {
    toast(`Could not get your matches. ${error.message}`); nextButton.innerHTML = "See my matches <span>↗</span>"; nextButton.disabled = false;
  }
}
function careerCard(career) {
  const matched = career.matched || [], saved = savedIds().includes(career.id);
  return `<article class="career-card"><div class="career-icon">${career.icon}</div><div><span class="career-category">${career.category}</span><h3>${career.title}</h3><p>${career.summary}</p>
    <div class="career-tags">${matched.slice(0, 4).map((tag) => `<span class="tag">${tag}</span>`).join("")}</div><div class="card-actions"><button class="small-action" data-details="${career.id}">Explore this path ↗</button></div></div>
    ${career.score ? `<span class="match-pill">${career.score}% match</span>` : ""}<button class="save-action${saved ? " saved" : ""}" data-save="${career.id}" aria-label="${saved ? "Remove" : "Save"} ${career.title}" title="Save career">${saved ? "♥" : "♡"}</button></article>`;
}
async function showCareerDetails(careerId) {
  openModal("<p>Loading career details…</p>");
  try {
    const career = await api(`/careers/${encodeURIComponent(careerId)}`), result = state.results.find((item) => item.id === careerId);
    const score = result ? `<p>Match score: ${result.score}% within this starter catalogue. This is a preference similarity score, not a success or employment probability.</p>` : "";
    const sources = career.sources.map((source) => `<li><a class="modal-link" href="${source.url}" target="_blank" rel="noopener">${source.title} ↗</a></li>`).join("");
    openModal(`<div class="modal-eyebrow">${career.category}</div><h2>${career.icon} ${career.title}</h2><p>${career.summary}</p><h3>A day in this path</h3><p>${career.day}</p><h3>A small way to explore</h3><p>${career.learn}</p><h3>Learning and qualifications</h3><p>${career.path}</p><h3>Sources to explore</h3><ul>${sources}</ul>${score}`);
  } catch (error) { openModal(`<h2>Could not load this career</h2><p>${error.message}</p>`); }
}
function renderSaved() {
  const saved = savedIds().map((id) => state.careers.find((career) => career.id === id)).filter(Boolean), list = $("#saved-list");
  list.innerHTML = saved.map((career) => careerCard({ ...career, score: 0, matched: [] })).join("");
  list.style.display = saved.length ? "grid" : "none"; $("#saved-empty").classList.toggle("visible", !saved.length);
}
function toggleSaved(id) {
  const ids = savedIds(), career = state.careers.find((item) => item.id === id); if (!career) return;
  setSaved(ids.includes(id) ? ids.filter((value) => value !== id) : [...ids, id]);
  toast(ids.includes(id) ? `${career.title} removed from saved careers` : `${career.title} saved for later`);
  if ($("#results-view").classList.contains("active")) $("#career-results").innerHTML = state.results.map(careerCard).join("");
  if ($("#saved-view").classList.contains("active")) renderSaved();
}
function shareResults() {
  const summary = `My AI Career Predictor exploration ideas:\n${state.results.slice(0, 3).map((career, index) => `${index + 1}. ${career.title} (${career.score}% match)`).join("\n")}\nExplore possibilities with AI Career Predictor.`;
  if (navigator.share) navigator.share({ title: "My career exploration ideas", text: summary }).catch(() => {});
  else if (navigator.clipboard) navigator.clipboard.writeText(summary).then(() => toast("Summary copied to clipboard")).catch(() => toast("Could not copy summary"));
  else toast("Sharing is not available in this browser");
}
function downloadResults() {
  const payload = { createdAt: new Date().toISOString(), note: "Exploration matches only; not a professional assessment or employment probability.", answers: state.answers, matches: state.results.map(({ id, title, category, score, matched }) => ({ id, title, category, score, matched })) };
  const url = URL.createObjectURL(new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" })), anchor = document.createElement("a");
  anchor.href = url; anchor.download = "ai-career-predictor-summary.json"; anchor.click(); URL.revokeObjectURL(url); toast("Your summary has been downloaded");
}
function about() {
  openModal(`<div class="modal-eyebrow">ABOUT AI CAREER PREDICTOR</div><h2 id="modal-title">A thoughtful place to <em>start.</em></h2><p>AI Career Predictor is a student career exploration project. It compares the interests and preferences you choose with tags in a small starter catalogue, then shows paths you may want to learn about.</p><h3>How the matches work</h3><p>Each career receives a weighted similarity score based on selected interests, strengths, subjects, work preferences, and priorities. The score is not a probability of career success or employment.</p><h3>Your privacy</h3><p>Your quiz answers are sent to the recommendation service to calculate matches and are not saved by this app. Saved careers stay in this browser.</p>`);
}
async function initialize() {
  $("#saved-count").textContent = savedIds().length;
  try { state.careers = await api("/careers"); }
  catch { toast("The website service is unavailable. Start the app using the setup steps in README.md."); }
}

$("#start-button").addEventListener("click", () => { state.step = 0; showView("quiz"); renderQuestion(); });
$("#saved-discover").addEventListener("click", () => showView("home")); $("#quit-quiz").addEventListener("click", () => showView("home"));
$("#prev-button").addEventListener("click", () => { if (state.step > 0) { state.step -= 1; renderQuestion(); } });
$("#next-button").addEventListener("click", () => { if (!state.answers[questions[state.step].key].length) return; if (state.step < questions.length - 1) { state.step += 1; renderQuestion(); } else renderResults(); });
$("#retake-button").addEventListener("click", () => { state.step = 0; state.answers = { interests: [], skills: [], subjects: [], work: [], priorities: [] }; showView("quiz"); renderQuestion(); });
$("#share-button").addEventListener("click", shareResults); $("#download-button").addEventListener("click", downloadResults);
$("#about-button").addEventListener("click", about); $("#method-button").addEventListener("click", about);
$("#modal-close").addEventListener("click", closeModal);
$("#modal-backdrop").addEventListener("click", (event) => { if (event.target === $("#modal-backdrop")) closeModal(); });
document.addEventListener("keydown", (event) => { if (event.key === "Escape" && !$("#modal-backdrop").hidden) closeModal(); });
$$('.nav-link').forEach((button) => button.addEventListener("click", () => showView(button.dataset.view)));
document.addEventListener("click", (event) => {
  const save = event.target.closest("[data-save]"); if (save) toggleSaved(save.dataset.save);
  const detail = event.target.closest("[data-details]"); if (detail) showCareerDetails(detail.dataset.details);
});
initialize();
