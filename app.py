import streamlit as st
import pandas as pd
import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(
    page_title="Smart Internship Recommender",
    page_icon="🚀",
    layout="wide"
)
st.markdown("""
<style>

/* App Background */
.stApp {
    background-color: #f4f7fc;
}

/* Main Title */
h1 {
    text-align: center;
    color: #1565C0;
    font-size: 42px;
    font-weight: bold;
}

/* Headings */
h2, h3 {
    color: #0D47A1;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #1565C0;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Input Box */
.stTextInput input {
    border-radius: 12px;
    border: 2px solid #1565C0;
}

/* Text Area */
.stTextArea textarea {
    border-radius: 12px;
    border: 2px solid #1565C0;
}

/* File Uploader */
[data-testid="stFileUploader"] {
    border: 2px dashed #1565C0;
    border-radius: 12px;
    background-color: white;
    padding: 15px;
}

/* Buttons */
.stButton > button {
    background-color: #1565C0;
    color: white;
    border-radius: 12px;
    border: none;
    height: 50px;
    width: 100%;
    font-size: 16px;
    font-weight: bold;
}

.stButton > button:hover {
    background-color: #0D47A1;
    color: white;
}

/* Progress Bar */
.stProgress > div > div > div > div {
    background-color: #1565C0;
}

/* Cards */
.custom-card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    margin-top: 10px;
    margin-bottom: 10px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    border-left: 5px solid #1565C0;
}

</style>
""", unsafe_allow_html=True)
st.sidebar.title("🚀 Smart Internship Recommender")

st.sidebar.info("""
AI Powered Career Guidance Platform
""")


st.sidebar.markdown("---")

st.sidebar.write("Features")

st.sidebar.write("✅ Resume Upload")
st.sidebar.write("✅ ML Recommendation")
st.sidebar.write("✅ Skill Gap Analysis")
st.sidebar.write("✅ Course Suggestions")
st.sidebar.write("✅ Career Roadmap")
st.sidebar.write("✅ AI Career Mentor")

st.title("🚀 Smart Internship Recommender")

# -----------------------------------
# Course Recommendation Database
# -----------------------------------

course_dict = {
    "python": "Python for Everybody - Coursera",
    "django": "Django for Beginners - Udemy",
    "sql": "SQL for Data Science - Coursera",
    "excel": "Excel Essentials - Coursera",
    "machine": "Machine Learning Specialization - Coursera",
    "learning": "Machine Learning Specialization - Coursera",
    "statistics": "Statistics for Data Science - Udemy",
    "deep": "Deep Learning Specialization - Coursera",
    "nlp": "Natural Language Processing - Coursera",
    "html": "HTML & CSS Bootcamp - Udemy",
    "css": "HTML & CSS Bootcamp - Udemy",
    "javascript": "JavaScript Complete Guide - Udemy",
    "react": "React Developer Course - Udemy",
    "mongodb": "MongoDB Developer Path - MongoDB University"
}

# -----------------------------------
# Resume Upload
# -----------------------------------

uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

resume_text = ""

if uploaded_file is not None:

    with pdfplumber.open(uploaded_file) as pdf:

        for page in pdf.pages:

            text = page.extract_text()

            if text:
                resume_text += text + " "

    st.success("✅ Resume uploaded successfully!")

    st.subheader("📄 Extracted Resume Text")

    st.text_area(
        "Resume Content",
        resume_text[:2000],
        height=200
    )

    skills = resume_text

else:

    skills = st.text_input(
        "Enter your skills"
    )

# -----------------------------------
# Internship Recommendation
# -----------------------------------

if st.button("Recommend"):

    if skills.strip() == "":

        st.warning(
            "Please upload a resume or enter skills."
        )

    else:

        df = pd.read_csv("internships.csv")

        all_text = df["Skills"].tolist()
        all_text.append(skills)

        vectorizer = TfidfVectorizer()

        vectors = vectorizer.fit_transform(
            all_text
        )

        similarity = cosine_similarity(
            vectors[-1],
            vectors[:-1]
        )

        df["Match Percentage"] = (
            similarity[0] * 100
        )

        result = df.sort_values(
            by="Match Percentage",
            ascending=False
        )

        st.subheader(
            "🏆 Top Recommended Internships"
        )

        for _, row in result.head(3).iterrows():

            st.write(
                f"## {row['Role']}"
            )
            st.markdown(
    f"""
    <div class="custom-card">
        <h3>{row['Role']}</h3>
    </div>
    """,
    unsafe_allow_html=True
)

            st.progress(
                int(row["Match Percentage"])
            )

            st.write(
                f"### Match Percentage: {row['Match Percentage']:.2f}%"
            )

            st.write(
                f"**Platform:** {row['Platform']}"
            )

            st.write(
                f"**Companies Hiring:** {row['Companies']}"
            )

            st.link_button(
                "🔗 Apply Here",
                row["Link"]
            )

            required = set(
                row["Skills"].lower().split()
            )

            student = set(
                skills.lower().split()
            )

            missing = required - student

            st.write("### Missing Skills")

            if missing:

                for skill in missing:
                    st.write(f"❌ {skill}")

            else:

                st.success(
                    "No Missing Skills 🎉"
                )

            # -----------------------------------
            # Course Recommendations
            # -----------------------------------

            st.write("### 📚 Recommended Courses")

            found_course = False

            for skill in missing:

                if skill in course_dict:

                    st.write(
                        f"✅ {skill.title()} → {course_dict[skill]}"
                    )

                    found_course = True

            if not found_course:

                st.write(
                    "No course recommendations available."
                )

            # -----------------------------------
            # Career Roadmap
            # -----------------------------------

            st.write("### 🗺️ Career Roadmap")

            st.write(
                "1️⃣ Learn the missing skills"
            )

            st.write(
                "2️⃣ Complete the recommended courses"
            )

            st.write(
                "3️⃣ Build projects using those skills"
            )

            for _, row in result.head(3).iterrows():

             st.markdown(
            f"""
            <div class="custom-card">
            <h3>{row['Role']}</h3>
            </div>
            """,
            unsafe_allow_html=True
            )

            st.write(
            f"5️⃣ Target companies: {row['Companies']}"
            )

  

            st.write(
                f"5️⃣ Target companies: {row['Companies']}"
            )

            st.divider()

# -----------------------------------
# AI Career Mentor
# -----------------------------------

st.subheader("🤖 AI Career Mentor")

question = st.text_input(
    "Ask a career question"
)

if st.button("Get Career Advice"):

    q = question.lower()

    if "ml" in q or "machine learning" in q:

        st.success("""
Roadmap to ML Engineer

1. Learn Python
2. Learn Statistics
3. Learn Machine Learning
4. Build ML Projects
5. Learn Deep Learning
6. Apply for ML Internships
7. Build a strong GitHub portfolio
        """)

    elif "backend" in q:

        st.success("""
Roadmap to Backend Developer

1. Learn Python
2. Learn Django
3. Learn REST APIs
4. Learn MongoDB
5. Build Backend Projects
6. Learn Deployment
7. Apply on Internshala & LinkedIn
        """)

    elif "data analyst" in q:

        st.success("""
Roadmap to Data Analyst

1. Learn Excel
2. Learn SQL
3. Learn Python
4. Learn Power BI
5. Build Dashboard Projects
6. Create a Portfolio
7. Apply for Analyst Internships
        """)

    elif "frontend" in q:

        st.success("""
Roadmap to Frontend Developer

1. Learn HTML
2. Learn CSS
3. Learn JavaScript
4. Learn React
5. Build Responsive Websites
6. Create Portfolio Projects
7. Apply for Frontend Internships
        """)

    else:

        st.info("""
General Career Advice

• Learn in-demand skills
• Build projects
• Earn certifications
• Improve communication skills
• Keep your LinkedIn updated
• Apply consistently
• Participate in hackathons
        """)