import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="LEGEND AI", page_icon="🧠", layout="wide")

st.markdown("""
<style>
.main-title {font-size: 42px; font-weight: 800; margin-bottom: 0;}
.subtitle {font-size: 18px; color: #888;}
</style>
""", unsafe_allow_html=True)

MODEL = "gpt-5.6-luna"

def get_client():
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
    except Exception:
        return None
    if not api_key or not str(api_key).strip():
        return None
    return OpenAI(api_key=str(api_key).strip())

def build_instructions(cls, stream, subject, language, mode):
    return f"""
You are LEGEND AI, a student-friendly academic learning assistant.

Student settings:
- Class: {cls}
- Stream/Area: {stream}
- Subject: {subject}
- Answer language: {language}
- Explanation level: {mode}

Rules:
1. Answer the student's actual question, not a generic demo message.
2. Explain clearly and accurately at the student's level.
3. If language is Hinglish, naturally mix simple Hindi and English.
4. If language is Hindi, use clear Hindi but keep standard scientific/mathematical terms in English where useful.
5. If language is English, answer in clear academic English.
6. For numerical problems, show the formula, substitution, calculation and final answer.
7. For science questions, use definitions, key points and equations where useful.
8. If the question is ambiguous, state the assumption you are making.
9. Never claim certainty when you are unsure. Encourage checking important answers with a textbook/teacher.
10. Keep answers student-friendly; use headings and bullets when they improve clarity.
"""

def ask_legend(question, cls, stream, subject, language, mode):
    client = get_client()

    if client is None:
        return (
            "⚠️ **AI backend is not connected yet.**\n\n"
            "Add `OPENAI_API_KEY` in Streamlit → Manage app → Settings → Secrets. "
            "Then reload the app."
        )

    try:
        response = client.responses.create(
            model=MODEL,
            instructions=build_instructions(cls, stream, subject, language, mode),
            input=question.strip(),
        )
        answer = response.output_text.strip()
        return answer if answer else "I couldn't generate an answer. Please try asking the question another way."
    except Exception as e:
        # Do not expose secret/key details in the UI.
        return (
            "⚠️ **I couldn't connect to the AI backend right now.**\n\n"
            "Please check the API key/usage settings in Streamlit Secrets and try again."
        )

st.markdown('<div class="main-title">🧠 LEGEND AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Student-Friendly Multilingual Learning Assistant</div>',
    unsafe_allow_html=True
)
st.divider()

with st.sidebar:
    st.header("⚙️ Study Settings")
    cls = st.selectbox("Class", ["9", "10", "11", "12", "Other"])
    stream = st.selectbox(
        "Stream / Area",
        ["Science", "Arts / Humanities", "Commerce", "General"]
    )

    subject_options = {
        "Science": ["Physics", "Chemistry", "Biology", "Maths"],
        "Arts / Humanities": [
            "History", "Political Science", "Geography",
            "Economics", "Sociology", "English", "Hindi"
        ],
        "Commerce": ["Accountancy", "Business Studies", "Economics", "Maths"],
        "General": ["General Knowledge", "English", "Maths"]
    }
    subject = st.selectbox("Subject", subject_options[stream])
    language = st.selectbox("Answer language", ["Hinglish", "Hindi", "English"])
    mode = st.radio("Explanation level", ["Simple", "Board Level", "Advanced"])

    if get_client() is not None:
        st.success("🤖 AI backend connected")
    else:
        st.warning("Demo mode: AI key not connected")

tab1, tab2, tab3 = st.tabs(["💬 Ask Doubt", "🧪 Practice", "ℹ️ About Project"])

with tab1:
    st.subheader("Ask your academic doubt")
    q = st.text_area(
        "Question",
        placeholder="Example: What is biodiversity? Explain it in Hinglish.",
        height=140
    )

    if st.button("🚀 Ask LEGEND AI", type="primary"):
        if not q.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("LEGEND AI is thinking..."):
                ans = ask_legend(q, cls, stream, subject, language, mode)

            st.markdown("### 🤖 LEGEND AI")
            st.markdown(ans)
            st.info(
                "Learning tip: concept ko apne words mein explain karke dekho. "
                "Important academic answers ko textbook/teacher se verify karna good practice hai."
            )

with tab2:
    st.subheader("Quick Practice")
    practice = {
        "Physics": [
            "What is electric dipole moment?",
            "What does a stationary charge produce?"
        ],
        "Chemistry": [
            "What is a salt bridge?",
            "Define oxidation state."
        ],
        "Biology": [
            "What is the function of tapetum?",
            "State one contribution of Mendel."
        ],
        "Maths": [
            "Write the quadratic formula."
        ]
    }
    questions = practice.get(
        subject,
        ["Write one important concept from this subject."]
    )
    for i, item in enumerate(questions, 1):
        st.write(f"**Q{i}.** {item}")

with tab3:
    st.subheader("Project Overview")
    st.write("""
    LEGEND AI is a school-level student learning assistant.
    It is designed to help students understand concepts, solve academic
    questions and practice subjects in a simple, personalized way.
    """)
    st.markdown("**Core technologies:** Python, Streamlit and an AI model API.")
    st.markdown(
        "**Important limitation:** AI can make mistakes. "
        "Students should verify important academic answers with textbooks, teachers and reliable sources."
    )
