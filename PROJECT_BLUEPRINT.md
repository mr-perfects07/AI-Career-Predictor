# AI Career Predictor — Project Blueprint

> Planning document for a college project. Complete the **Decisions to confirm** section before collecting data or building the recommendation logic.

## 1. Project summary

**Working title:** AI Career Predictor  
**Goal:** Help students explore career options that may fit their interests, skills, subjects, and work preferences.  
**Intended users:** Students exploring career paths.  
**Project type:** Python backend with a web frontend.  
**Recommendation promise:** Suggestions are exploratory, explainable matches—not a guarantee of career success or a professional assessment.

## 2. Problem and proposed solution

Students may know their favorite subjects or activities but not the careers connected to them. The app will collect a short set of preferences, compare them with a documented career catalogue, and return a ranked set of options with clear reasons and suggested next steps.

## 3. First release scope

### In scope

- A landing page that explains the tool and starts the questionnaire.
- A questionnaire about interests, skills, subjects, work preferences, and priorities.
- A career catalogue with tags and cited information sources.
- Ranked career suggestions with match explanations.
- Career detail pages with education/skill context and exploration steps.
- A short “How recommendations work” and limitations section.
- Responsive frontend and a Python JSON API.

### Later options

- User accounts and saved profiles.
- A student dashboard and saved comparisons.
- A trained machine-learning model, if an appropriate dataset is found and its use can be justified.
- Region-specific education pathways and localized career information.

## 4. Decisions to confirm

| Decision | Current proposal | Confirm / notes |
|---|---|---|
| Country or region covered | To be decided before sourcing career and education data | |
| Target student group | High-school / college / other | |
| First catalogue size | Start with 20–30 careers | |
| User accounts | No accounts in first release; process answers without retaining them | |
| Database | PostgreSQL if persistent data is needed; static JSON/CSV is fine for the first prototype | |
| Recommendation approach | Explainable weighted matching for version one | |
| Frontend framework | Next.js or React | |
| Python API framework | FastAPI | |
| Hosting | Frontend on Vercel; deploy Python API and database on compatible managed services | |
| Project requirement | Confirm whether coursework requires a specific ML model or database | |

## 5. User journey

1. Student opens the home page and reads what the tool does.
2. Student completes the questionnaire.
3. Frontend sends answers to the Python API.
4. API validates answers and scores each career in the catalogue.
5. Results page shows the top matches, score context, and matching answers.
6. Student opens a career detail page to see sources and suggested exploration steps.

## 6. Information to collect

### Student questionnaire

Keep questions relevant to matching and avoid collecting identifying information.

| Field | Example answer type | Why it helps |
|---|---|---|
| Education stage | Select one | Tailors suggested next steps |
| Enjoyed subjects | Multi-select | Connects academic interests |
| Activities enjoyed | Multi-select | Captures interests beyond subjects |
| Skills / strengths | Multi-select | Finds skill overlap |
| Preferred work activities | Multi-select | Matches day-to-day work |
| Work setting preference | Multi-select / optional | Adds context to suggestions |
| Career priorities | Rank or select up to three | Lets priorities influence ranking |

For every question, document its ID, exact wording, answer choices, whether it is optional, and which career tags it maps to.

### Career catalogue

Create one record per career. Suggested fields:

- career_id — stable unique ID
- title and category
- summary
- interests — normalized tags
- skills — normalized tags
- subjects — normalized tags
- work_activities and work_environment
- education_notes — region-specific and carefully sourced
- exploration_steps — practical ways to learn more
- sources — title, publisher, URL, access date
- reviewed_at

Keep the source and date with every factual career or education claim. Requirements vary by location and can change.

## 7. Recommendation method for version one

Use a transparent weighted score rather than claiming the result is a definitive prediction.

Example starting weights (tune after reviewing sample cases):

- Interests: 35%
- Skills: 25%
- Subjects: 20%
- Work preferences: 15%
- Career priorities: 5%

For each career, calculate the weighted proportion of selected tags that match its catalogue tags. Normalize scores to a consistent range, rank careers, and return the strongest few. If no career has enough overlap, say so and invite the student to explore broader options.

Each result should include:
- Career title and match score.
- Which answers contributed to the match.
- A short plain-language explanation.
- A link to the career detail and its sources.

Document the scoring formula and weights in the report. A score is a similarity indicator within this catalogue, not a probability of success or employability.

## 8. Suggested architecture

- **Frontend:** Next.js or React, deployed on Vercel.
- **Backend:** FastAPI application in Python, deployed separately.
- **Database:** PostgreSQL for durable career records or saved profiles. The first prototype can load careers from JSON/CSV.
- **API:** JSON over HTTPS; configure the frontend API URL through an environment variable.
- **Secrets:** Keep database credentials and API secrets on the backend host. Never expose them in frontend code or commit them to GitHub.

### Initial API endpoints

| Method | Route | Purpose |
|---|---|---|
| GET | /health | Deployment health check |
| GET | /questions | Return questionnaire definitions |
| GET | /careers | List career catalogue |
| GET | /careers/{career_id} | Career details and source references |
| POST | /recommend | Validate answers and return ranked matches |

## 9. Data storage and privacy

- Prefer anonymous, temporary recommendations in the first release.
- Do not save questionnaire answers unless a feature requires them.
- If profiles are added later, explain what is stored and provide deletion.
- Collect only what is needed to produce recommendations.
- Do not store sensitive personal information in the career dataset or logs.
- Keep secrets out of source control; use environment variables and an example env file with placeholder names only.

## 10. Career data collection checklist

For each career:

- [ ] Confirm the career is relevant to the selected region and student group.
- [ ] Write a neutral summary in your own words.
- [ ] Add consistent interest, skill, subject, activity, and priority tags.
- [ ] Verify education and qualification notes against a reliable source.
- [ ] Save source title, publisher, URL, and date checked.
- [ ] Check that claims are current and avoid unsupported salary promises.
- [ ] Have another person review tag assignments for obvious bias or gaps.

Possible source types include official occupational information, education institutions, professional associations, and government career resources. Select sources for the target region and cite each record.

## 11. Suggested repository layout

~~~text
AI-Career-Predictor/
├── README.md
├── PROJECT_BLUEPRINT.md
├── frontend/
├── backend/
│   ├── app/
│   ├── data/
│   └── requirements.txt
├── docs/
└── .gitignore
~~~

Adapt this layout to the frameworks and deployment setup you choose. Do not commit secrets, virtual environments, build outputs, or private student responses.

## 12. Build milestones

1. Confirm region, target users, coursework requirements, and account/storage needs.
2. Finalize questions and tag vocabulary.
3. Gather and cite an initial set of career records.
4. Implement the scoring function and manually inspect example outcomes.
5. Build the FastAPI endpoints and validate request/response formats.
6. Build the frontend questionnaire, results, and detail views.
7. Connect frontend to the deployed API; configure CORS and environment variables.
8. Add PostgreSQL only if the chosen features need persistence.
9. Deploy, document setup, and prepare a project demonstration.
10. Write the report: problem, data sources, method, architecture, evaluation, limitations, and future work.

## 13. Evaluation checklist

- Can a student finish the questionnaire without confusion?
- Do recommendations change sensibly when answers change?
- Can each result explain which answers contributed?
- Are career information and education claims linked to sources?
- Does the API handle missing or invalid answers clearly?
- Does the deployed frontend communicate with the backend?
- Are privacy behavior and recommendation limitations visible?
- Does the report explain how the score is calculated?

## 14. Risks and limits

- A small catalogue cannot represent every career.
- Tags and weights reflect design choices and may encode bias.
- Similarity scores are not validated probabilities or employment forecasts.
- Education and licensing requirements are region-specific.
- Career data can become outdated and needs periodic review.

## 15. Information gathering worksheet

Fill this in before implementation:

- **Project rubric / required features:**
- **Target country or region:**
- **Target student group:**
- **Required AI or ML technique, if any:**
- **Required database, if any:**
- **Preferred frontend framework:**
- **Careers to include initially:**
- **Sources available through college/library:**
- **Whether the app should save results:**
- **Expected demo date:**
