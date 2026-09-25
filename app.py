import streamlit as st
from pathlib import Path
import re

st.set_page_config(page_title="LEGEND AI", page_icon="🧠", layout="wide")

st.markdown("""
<style>
.main-title {font-size: 42px; font-weight: 800; margin-bottom: 0;}
.subtitle {font-size: 18px; color: #666;}
.card {padding: 18px; border-radius: 14px; border: 1px solid #ddd; margin-bottom: 12px;}
</style>
""", unsafe_allow_html=True)

# Demo knowledge base: intentionally limited and transparent for school demonstration.
DEMO = {
    "physics": {
        "electric dipole": "An electric dipole consists of two equal and opposite charges separated by a small distance. Its dipole moment is p = q × 2a and its direction is from negative charge to positive charge.",
        "stationary charge": "A stationary electric charge produces an electric field. In the ideal electrostatic case, it does not produce a magnetic field due to motion."
    },
    "chemistry": {
        "salt bridge": "A salt bridge completes the electrical circuit and maintains electrical neutrality by allowing ions to migrate between the half-cells. It also reduces direct mixing of the two solutions.",
        "oxidation state": "Oxidation state is the hypothetical charge assigned to an atom in a compound according to conventional rules."
    },
    "biology": {
        "tapetum": "Tapetum is the innermost layer of the anther wall. It provides nourishment to developing pollen grains and contributes materials needed for pollen-wall formation.",
        "mendel": "Mendel studied inheritance using pea plants. His work led to principles such as segregation and independent assortment."
    },
    "maths": {
        "quadratic": "For ax² + bx + c = 0, the quadratic formula is x = (-b ± √(b² − 4ac)) / 2a."
    }
}

def demo_answer(q, subject):
    ql = q.lower()
    # exact-ish topic lookup
    for topic, ans in DEMO.get(subject.lower(), {}).items():
        if topic in ql:
            return ans
    if any(x in ql for x in ["hello", "hi", "namaste"]):
        return "Namaste! 👋 Main LEGEND AI hoon. Apna academic doubt poochho."
    return ("Demo mode mein main selected school topics ke examples par answer de raha hoon. "
            "Full AI answers ke liye app ko an AI API/model ke saath connect kiya ja sakta hai. "
            "Aap subject, class aur question clearly enter karein.")

def get_ai_answer(question, subject, cls, language, mode):
    # Optional API integration hook. Kept offline by default for school demo.
    api_key = st.session_state.get("api_key", "").strip()
    if not api_key:
        return demo_answer(question, subject)
    # No vendor-specific network call is made in the school starter.
    return demo_answer(question, subject) + "\n\nAPI key detected, but the starter is intentionally offline. Connect your chosen provider in the integration section of the README."

st.markdown('<div class="main-title">🧠 LEGEND AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Student-Friendly Multilingual Learning Assistant</div>', unsafe_allow_html=True)
st.divider()

with st.sidebar:
    st.header("⚙️ Study Settings")
    cls = st.selectbox("Class", ["9", "10", "11", "12", "Other"])
    stream = st.selectbox("Stream / Area", ["Science", "Arts / Humanities", "Commerce", "General"])
    subject_options = {
        "Science": ["Physics", "Chemistry", "Biology", "Maths"],
        "Arts / Humanities": ["History", "Political Science", "Geography", "Economics", "Sociology", "English", "Hindi"],
        "Commerce": ["Accountancy", "Business Studies", "Economics", "Maths"],
        "General": ["General Knowledge", "English", "Maths"]
    }
    subject = st.selectbox("Subject", subject_options[stream])
    language = st.selectbox("Answer language", ["Hinglish", "Hindi", "English"])
    mode = st.radio("Explanation level", ["Simple", "Board Level", "Advanced"])
    st.session_state["api_key"] = st.text_input("Optional AI API key", type="password", help="Leave blank for offline school demo.")
    st.caption("Privacy note: do not enter personal/sensitive information.")

tab1, tab2, tab3 = st.tabs(["💬 Ask Doubt", "🧪 Practice", "ℹ️ About Project"])

with tab1:
    st.subheader("Ask your academic doubt")
    q = st.text_area("Question", placeholder="Example: Electric dipole ka torque Hinglish mein samjhao.", height=120)
    if st.button("🚀 Ask LEGEND AI", type="primary"):
        if not q.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Thinking..."):
                ans = get_ai_answer(q, subject, cls, language, mode)
            st.markdown("### 🤖 LEGEND AI")
            st.write(ans)
            st.info("Learning tip: Formula/definition ko yaad karne ke saath concept ko apne words mein explain karke dekho.")

with tab2:
    st.subheader("Quick Practice")
    practice = {
        "Physics": ["What is electric dipole moment?", "What does a stationary charge produce?"],
        "Chemistry": ["What is a salt bridge?", "Define oxidation state."],
        "Biology": ["What is the function of tapetum?", "State one contribution of Mendel."],
        "Maths": ["Write the quadratic formula."]
    }
    questions = practice.get(subject, ["Write one important concept from this subject."])
    for i, item in enumerate(questions, 1):
        st.write(f"**Q{i}.** {item}")
    st.caption("Teacher can expand this section with chapter-wise question banks.")

with tab3:
    st.subheader("Project Overview")
    st.write("""
    LEGEND AI is a school-level prototype of a student-friendly learning assistant.
    It is designed mainly for Science students, with Arts/Humanities and Commerce support.
    Students can choose their class, subject, language and explanation level before asking a doubt.
    """)
    st.markdown("**Core technologies:** Python, Streamlit, optional AI model/API integration.")
    st.markdown("**Important limitation:** AI systems can make mistakes. Students should verify important academic answers with textbooks, teachers and reliable sources.")
