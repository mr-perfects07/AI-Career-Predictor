"""Shared question and career data plus scoring logic."""

QUESTIONS = [
    {
        "key": "interests",
        "title": "What kinds of things pull you in?",
        "max_selections": 3,
        "options": [
            "design", "people", "data", "technology", "nature",
            "communication", "building", "learning", "problem solving",
        ],
    },
    {
        "key": "skills",
        "title": "What do people often count on you for?",
        "max_selections": 3,
        "options": [
            "creativity", "analytical thinking", "communication", "empathy",
            "organization", "curiosity", "problem solving",
        ],
    },
    {
        "key": "subjects",
        "title": "Which subjects feel most like your zone?",
        "max_selections": 3,
        "options": [
            "mathematics", "computer science", "biology", "chemistry",
            "art and design", "psychology", "business",
            "language and literature", "geography", "economics",
        ],
    },
    {
        "key": "work",
        "title": "What kind of workday sounds good?",
        "max_selections": 2,
        "options": [
            "creating", "research", "helping others", "collaboration",
            "independent focus", "communication", "problem solving",
        ],
    },
    {
        "key": "priorities",
        "title": "What would you like your future work to offer?",
        "max_selections": 2,
        "options": [
            "helping others", "creativity", "learning", "stability", "flexibility",
        ],
    },
]

CAREERS = [
    {
        "id": "ux-designer", "title": "UX / Product Designer", "category": "DESIGN & TECHNOLOGY", "icon": "✳",
        "summary": "Shape digital products around the needs of real people. Research, sketch, test ideas, and work with a team to make useful experiences.",
        "interests": ["design", "people", "technology", "problem solving"],
        "skills": ["creativity", "communication", "empathy", "problem solving"],
        "subjects": ["art and design", "computer science", "psychology"],
        "work": ["collaboration", "creating", "research"],
        "priorities": ["creativity", "helping others"],
        "day": "A typical day might include interviewing users, mapping a journey, sketching screen ideas, and sharing a prototype with a product team.",
        "learn": "Try redesigning a familiar app screen, then ask a few people to try it and tell you where they get stuck.",
        "path": "Many people enter through design, interaction design, human-computer interaction, or portfolio-based learning. Paths vary by region and employer.",
        "sources": [{"title": "U.S. Bureau of Labor Statistics — Web Developers and Digital Designers", "url": "https://www.bls.gov/ooh/computer-and-information-technology/web-developers.htm"}, {"title": "Interaction Design Foundation — UX Design", "url": "https://www.interaction-design.org/literature/topics/ux-design"}],
    },
    {
        "id": "data-analyst", "title": "Data Analyst", "category": "DATA & INSIGHT", "icon": "⌁",
        "summary": "Turn information into clearer decisions. Analysts explore patterns, ask good questions, and explain what the numbers may be telling us.",
        "interests": ["data", "problem solving", "technology", "research"],
        "skills": ["analytical thinking", "curiosity", "communication", "organization"],
        "subjects": ["mathematics", "computer science", "economics"],
        "work": ["research", "problem solving", "independent focus"],
        "priorities": ["learning", "stability"],
        "day": "You might clean a dataset, look for trends, build a chart, and explain the takeaway to people who need to make a decision.",
        "learn": "Pick an open dataset you care about, make three simple charts, and write one sentence about each pattern you notice.",
        "path": "Common starting points include statistics, mathematics, economics, computer science, or practical portfolio work. Tools and requirements vary.",
        "sources": [{"title": "U.S. Bureau of Labor Statistics — Data Scientists", "url": "https://www.bls.gov/ooh/math/data-scientists.htm"}, {"title": "Google — Data Analytics Certificate overview", "url": "https://grow.google/certificates/data-analytics/"}],
    },
    {
        "id": "software-developer", "title": "Software Developer", "category": "ENGINEERING & TECHNOLOGY", "icon": "⌘",
        "summary": "Build tools and experiences with code. Developers break big problems into smaller pieces and collaborate to make software useful and reliable.",
        "interests": ["technology", "problem solving", "building", "independent focus"],
        "skills": ["analytical thinking", "curiosity", "organization", "problem solving"],
        "subjects": ["computer science", "mathematics", "physics"],
        "work": ["creating", "problem solving", "collaboration"],
        "priorities": ["learning", "flexibility"],
        "day": "A day could involve understanding a feature request, writing and reviewing code, fixing an issue, and working with teammates on a release.",
        "learn": "Build a tiny tool that solves an everyday annoyance, such as a study timer or reading list.",
        "path": "Computer science and software engineering are common routes, but practical projects, apprenticeships, and other learning paths also exist.",
        "sources": [{"title": "U.S. Bureau of Labor Statistics — Software Developers", "url": "https://www.bls.gov/ooh/computer-and-information-technology/software-developers.htm"}],
    },
    {
        "id": "psychologist", "title": "Psychologist", "category": "PEOPLE & WELLBEING", "icon": "◌",
        "summary": "Study how people think, feel, and behave. Psychologists use evidence and careful listening to support people or improve programs and services.",
        "interests": ["people", "research", "helping others", "learning"],
        "skills": ["empathy", "communication", "curiosity", "analytical thinking"],
        "subjects": ["psychology", "biology", "sociology"],
        "work": ["helping others", "research", "communication"],
        "priorities": ["helping others", "learning"],
        "day": "Depending on the role, you may conduct research, assess needs, work with clients, or help organizations understand behavior.",
        "learn": "Explore an introductory psychology lecture and compare research, clinical, school, and workplace psychology roles.",
        "path": "Training and licensing requirements vary substantially by country and specialty. Check local official education and licensing sources.",
        "sources": [{"title": "U.S. Bureau of Labor Statistics — Psychologists", "url": "https://www.bls.gov/ooh/life-physical-and-social-science/psychologists.htm"}],
    },
    {
        "id": "teacher", "title": "Teacher / Learning Designer", "category": "EDUCATION & COMMUNITY", "icon": "✎",
        "summary": "Help people understand ideas and grow their confidence. Teaching can happen in classrooms, online programs, museums, and many other settings.",
        "interests": ["people", "learning", "creating", "helping others"],
        "skills": ["communication", "empathy", "organization", "creativity"],
        "subjects": ["education", "psychology", "language and literature"],
        "work": ["teaching", "communication", "collaboration"],
        "priorities": ["helping others", "creativity"],
        "day": "You could plan a lesson, explain a concept in different ways, guide a group activity, and notice what helps each learner move forward.",
        "learn": "Choose a topic you know well and teach it to a friend in three different ways: a sketch, a story, and a short explanation.",
        "path": "Teaching qualifications, subject requirements, and registration are location-specific. Learning design roles can have different entry routes.",
        "sources": [{"title": "U.S. Bureau of Labor Statistics — High School Teachers", "url": "https://www.bls.gov/ooh/education-training-and-library/high-school-teachers.htm"}],
    },
    {
        "id": "environmental-scientist", "title": "Environmental Scientist", "category": "SCIENCE & SUSTAINABILITY", "icon": "❋",
        "summary": "Use science to understand environmental challenges and help communities, organizations, or governments make informed choices.",
        "interests": ["nature", "research", "problem solving", "helping others"],
        "skills": ["analytical thinking", "curiosity", "organization", "communication"],
        "subjects": ["biology", "chemistry", "geography"],
        "work": ["research", "field work", "problem solving"],
        "priorities": ["helping others", "learning"],
        "day": "Work may combine field observations, sample analysis, writing reports, and explaining findings to colleagues or communities.",
        "learn": "Look up a local environmental issue and map who studies it, what data is gathered, and what decisions depend on it.",
        "path": "Environmental science, biology, chemistry, or related fields are common study areas. Roles differ in fieldwork and specialization.",
        "sources": [{"title": "U.S. Bureau of Labor Statistics — Environmental Scientists and Specialists", "url": "https://www.bls.gov/ooh/life-physical-and-social-science/environmental-scientists-and-specialists.htm"}],
    },
    {
        "id": "marketing-strategist", "title": "Marketing Strategist", "category": "BUSINESS & COMMUNICATION", "icon": "↗",
        "summary": "Connect an idea with the people who may value it. Marketing teams research audiences, shape messages, and learn from campaign results.",
        "interests": ["communication", "people", "creating", "data"],
        "skills": ["creativity", "communication", "curiosity", "organization"],
        "subjects": ["business", "language and literature", "economics"],
        "work": ["communication", "collaboration", "research"],
        "priorities": ["creativity", "flexibility"],
        "day": "You might learn about an audience, brainstorm a campaign, write or review content, and check what people responded to.",
        "learn": "Pick a product you like and write down who it helps, what problem it solves, and how you would introduce it to someone new.",
        "path": "Marketing, communications, business, and portfolio projects are common starting points. Roles vary from creative to analytical.",
        "sources": [{"title": "U.S. Bureau of Labor Statistics — Market Research Analysts", "url": "https://www.bls.gov/ooh/business-and-financial/market-research-analysts.htm"}],
    },
    {
        "id": "healthcare-professional", "title": "Healthcare Professional", "category": "HEALTH & WELLBEING", "icon": "✚",
        "summary": "Support people’s health through care, prevention, research, or health services. This broad field includes many distinct roles and training paths.",
        "interests": ["people", "helping others", "biology", "problem solving"],
        "skills": ["empathy", "communication", "organization", "analytical thinking"],
        "subjects": ["biology", "chemistry", "psychology"],
        "work": ["helping others", "communication", "teamwork"],
        "priorities": ["helping others", "stability"],
        "day": "The day-to-day depends on the role: it may include patient support, health education, lab work, care coordination, or clinical practice.",
        "learn": "Compare two healthcare roles and note how their daily tasks and training routes differ in your region.",
        "path": "Education, registration, and licensing requirements depend on the specific role and country. Verify details with local official sources.",
        "sources": [{"title": "U.S. Bureau of Labor Statistics — Healthcare Occupations", "url": "https://www.bls.gov/ooh/healthcare/home.htm"}],
    },
    {
        "id": "architect", "title": "Architect", "category": "DESIGN & BUILT ENVIRONMENT", "icon": "⌂",
        "summary": "Imagine and plan the spaces people live, learn, and work in. Architects balance creativity with practical, technical, and community needs.",
        "interests": ["design", "building", "problem solving", "people"],
        "skills": ["creativity", "analytical thinking", "organization", "communication"],
        "subjects": ["art and design", "mathematics", "physics"],
        "work": ["creating", "collaboration", "problem solving"],
        "priorities": ["creativity", "helping others"],
        "day": "You might develop design concepts, create drawings or models, coordinate with engineers, and refine plans around a client’s needs.",
        "learn": "Sketch a space that solves a real need, then list the users, constraints, materials, and questions you would investigate.",
        "path": "Accreditation, supervised experience, and licensure requirements are specific to each country. Check the local architecture regulator.",
        "sources": [{"title": "U.S. Bureau of Labor Statistics — Architects", "url": "https://www.bls.gov/ooh/architecture-and-engineering/architects.htm"}],
    },
    {
        "id": "entrepreneur", "title": "Entrepreneur / Founder", "category": "BUILDING & BUSINESS", "icon": "↗",
        "summary": "Bring a useful idea to life by understanding a need, testing a solution, and learning how to make it sustainable.",
        "interests": ["building", "creating", "people", "problem solving"],
        "skills": ["creativity", "curiosity", "communication", "organization"],
        "subjects": ["business", "economics", "computer science"],
        "work": ["creating", "collaboration", "problem solving"],
        "priorities": ["flexibility", "creativity"],
        "day": "A founder’s work changes often: learning from potential users, testing an idea, making plans, and bringing people together around a goal.",
        "learn": "Ask five people about one small problem they experience, then sketch a low-cost way to test a possible solution.",
        "path": "There is no single required degree or path. Business, design, technology, and industry experience can all be useful.",
        "sources": [{"title": "U.S. Small Business Administration — Plan your business", "url": "https://www.sba.gov/business-guide/plan-your-business"}],
    },
]

WEIGHTS = {"interests": 3.0, "skills": 2.4, "subjects": 1.6, "work": 1.4, "priorities": 0.8}
QUESTION_BY_KEY = {question["key"]: question for question in QUESTIONS}

def validate_answers(answers):
    if not isinstance(answers, dict):
        raise ValueError("Answers must be an object")
    if set(answers) != set(WEIGHTS):
        raise ValueError("Provide selections for all five question categories")
    for key, question in QUESTION_BY_KEY.items():
        values = answers[key]
        if not isinstance(values, list) or not 1 <= len(values) <= question["max_selections"]:
            raise ValueError(f"Choose between 1 and {question['max_selections']} options for {key}")
        if not all(isinstance(value, str) for value in values):
            raise ValueError(f"Selections for {key} must be text values")
        if len(values) != len(set(values)):
            raise ValueError(f"Duplicate selections are not allowed for {key}")
        unknown = set(values) - set(question["options"])
        if unknown:
            raise ValueError(f"Unsupported selections for {key}: {', '.join(sorted(unknown))}")
    return answers

def public_career(career, include_details=False):
    fields = ("id", "title", "category", "icon", "summary")
    result = {key: career[key] for key in fields}
    if include_details:
        result.update({key: career[key] for key in ("day", "learn", "path", "sources")})
    return result

def recommend(answers):
    validate_answers(answers)
    possible = sum(WEIGHTS.values())
    ranked = []
    for career in CAREERS:
        score = 0.0
        matched = []
        for key, weight in WEIGHTS.items():
            selected = answers[key]
            overlaps = [value for value in selected if value in career[key]]
            score += weight * len(overlaps) / len(selected)
            matched.extend(overlaps)
        ranked.append({
            **public_career(career),
            "score": round(score / possible * 100),
            "matched": list(dict.fromkeys(matched)),
        })
    ranked.sort(key=lambda item: (-item["score"], item["title"]))
    return {"matches": ranked[:5], "note": "Similarity within this starter catalogue; not a probability of career success or employment."}
