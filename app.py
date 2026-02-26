import streamlit as st
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

# -------------------------
# Page Config
# -------------------------
st.set_page_config(page_title="AI Resume Builder", page_icon="💼", layout="wide")

# -------------------------
# Theme Toggle
# -------------------------
if "theme" not in st.session_state:
    st.session_state.theme = "Light"

col1, col2 = st.columns([8, 1])

with col2:
    if st.button("🌙 / ☀ Toggle"):
        if st.session_state.theme == "Light":
            st.session_state.theme = "Dark"
        else:
            st.session_state.theme = "Light"

# -------------------------
# Apply Theme
# -------------------------

if st.session_state.theme == "Light":
    background_style = """
        background: linear-gradient(135deg, #F08080 ,#a6c1ee,#008B8B);
    """
    font_color = "#1e1e1e"
    heading_color = "#000000"

else:
    background_style = """
        background: linear-gradient(135deg, #2F4F4F, #778899,#008080);
    """
    font_color = "#7BC2DC"        # normal text color
    heading_color = "#C19054"     # cyan headings (you can change this)

st.markdown(f"""
    <style>

    .stApp {{
        {background_style}
    }}

    /* Main Title */
    h1 {{
        font-size: 48px !important;
        font-weight: 800 !important;
        text-align: center;
        color: {heading_color} !important;
    }}

    /* Section Headings */
    h2, h3 {{
        color: {heading_color} !important;
    }}

    /* Normal Text */
    p, label, div {{
        font-size: 17px !important;
        font-weight: 500 !important;
        color: {font_color} !important;
    }}

    </style>
""", unsafe_allow_html=True)

# -------------------------
# Load ML Model
# -------------------------
model = pickle.load(open("resume_model.pkl", "rb"))
vectorizer = pickle.load(open("resume_vectorizer.pkl", "rb"))

st.markdown("<h1>💼 AI Resume & Portfolio Builder</h1>", unsafe_allow_html=True)

st.write("Generate smart resumes, portfolio pages, and cover letters using AI & ML.")

# -------------------------
# User Inputs
# -------------------------

template_choice = st.selectbox(
    "Choose Resume Template",
    ["Modern Professional", "Minimal Clean", "Creative Bold"]
)

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    skills = st.text_area("Skills (comma separated)")
    education = st.text_area("Education")

with col2:
    projects = st.text_area("Projects (each on new line)")
    experience = st.text_area("Work Experience")
    career_goal = st.text_area("Career Objective")
    linkedin = st.text_input("LinkedIn URL")
    github = st.text_input("GitHub URL")

# -------------------------
# Skill Suggestions
# -------------------------

skill_suggestions = {
    "Data Science": ["NumPy", "Matplotlib", "Scikit-learn"],
    "Web Development": ["TypeScript", "MongoDB", "Express.js"],
    "AI/ML": ["Keras", "PyTorch", "Computer Vision"],
    "Cybersecurity": ["SIEM", "Linux Security", "Risk Assessment"],
    "Marketing": ["Google Ads", "Analytics", "Email Marketing"]
}

# -------------------------
# Generate Resume
# -------------------------


if st.button("🚀 Generate Resume & Portfolio"):

    if not skills.strip():
        st.error("Please enter skills.")
    else:

        input_vector = vectorizer.transform([skills])
        predicted_domain = model.predict(input_vector)[0]
        

        skill_count = len([s for s in skills.split(",") if s.strip()])
        project_count = len([p for p in projects.split("\n") if p.strip()])
        score = min(100, (skill_count * 4) + (project_count * 12))

        display_name = name if name.strip() else "This candidate"

        summary = f"""
        {display_name} is a dedicated {predicted_domain} professional with strong expertise in {skills}.
        Passionate about applying innovative solutions to real-world challenges.
        """
        # -------------------------
# Cover Letter Generation
# -------------------------

cover_letter = f"""
Dear Hiring Manager,

I am excited to apply for opportunities in {predicted_domain}. 
With strong skills in {skills}, I have worked on projects like {projects.split(chr(10))[0] if projects else "various academic projects"}.

My education in {education} and hands-on experience have prepared me to contribute effectively to your organization.

I am confident that my passion and technical abilities will add value to your team.

Sincerely,
{display_name}
"""

if template_choice == "Modern Professional":
    resume_format = f"""
====================================
{display_name.upper()}
====================================
Email: {email} | Phone: {phone}

CAREER OBJECTIVE
{career_goal}

EDUCATION
{education}

SKILLS
{skills}

PROJECTS
{projects}

EXPERIENCE
{experience}
"""
elif template_choice == "Minimal Clean":
    resume_format = f"""
{display_name}
-----------------------
Email: {email}
Phone: {phone}

Objective:
{career_goal}

Education:
{education}

Skills:
{skills}

Projects:
{projects}
"""
else:
    resume_format = f"""
🔥 {display_name} 🔥

📧 {email} | 📱 {phone}

🚀 About Me:
{summary}

🎓 Education:
{education}

💡 Skills:
{skills}

📌 Projects:
{projects}

💼 Experience:
{experience}
"""

portfolio_page = f"""
        <div style='padding:20px; background:white; border-radius:10px;'>
        <h2>{display_name}'s Portfolio</h2>
        <p><b>Domain:</b> {predicted_domain}</p>
        <p><b>Skills:</b> {skills}</p>
        <p><b>Projects:</b><br>{projects.replace(chr(10), '<br>')}</p>
        <p><b>LinkedIn:</b> {linkedin}</p>
        <p><b>GitHub:</b> {github}</p>
        </div>
        """

st.divider()

st.subheader("🎯 Predicted Domain")
st.success(predicted_domain)

st.subheader("📊 Resume Strength Score")
st.progress(score / 100)
st.write(f"Score: {score}%")

st.subheader("💡 Recommended Skills")
for s in skill_suggestions.get(predicted_domain, []):
            st.write("•", s)

st.subheader("📝 Professional Summary")
st.info(summary)

st.subheader("📄 Generated Resume")
st.code(resume_format)

st.subheader("📩 Generated Cover Letter")
st.text_area("Cover Letter", cover_letter, height=250)

st.subheader("🌐 Portfolio Preview")
st.markdown(portfolio_page, unsafe_allow_html=True)

st.success("✅ Resume , Cover Letter & Portfolio Generated Successfully!")