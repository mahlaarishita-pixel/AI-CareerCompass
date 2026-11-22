import re
import io
import streamlit as st
from pypdf import PdfReader

st.set_page_config(page_title="AI CareerCompass", page_icon="🧭", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
html, body, [class*="css"] {font-family:'DM Sans',sans-serif;}
.main {background:#f5f8f5;}
.hero {padding:1.2rem 0 1rem 0;}
.hero h1 {font-family:Manrope,sans-serif;font-size:3rem;line-height:1.08;font-weight:800;color:#17211e;}
.hero h1 span {color:#1d6c50;}
.smallcap {letter-spacing:2px;font-size:.72rem;font-weight:700;color:#1d6c50;}
div[data-testid="stMetric"] {background:white;padding:18px;border:1px solid #dce5df;border-radius:14px;}
.result-card {background:white;border:1px solid #dce5df;border-radius:14px;padding:18px;margin:8px 0;}
.pill {display:inline-block;background:#dff2e8;color:#1d6c50;border-radius:20px;padding:5px 10px;margin:4px;font-size:.85rem;}
.warn {background:#fff7e9;border-left:4px solid #e4a45d;padding:12px;border-radius:8px;}
</style>
""", unsafe_allow_html=True)

MASTER_PROMPT = """You are AI CareerCompass, a careful resume-to-job-description reviewer.
Use ONLY facts explicitly present in the resume. Never invent skills, employers, projects,
metrics, dates, degrees, certifications, or experience. Distinguish evidence from inference.
Compare the resume with the job description and return a match score with a transparent rubric,
evidenced matching skills, required skills not evidenced, evidence gaps, truthful rewritten bullet
suggestions using placeholders where facts are missing, and an action plan. If either input is
missing or too short, ask for the missing material. Do not expose private contact details.
Rubric: required skills evidence 40, responsibilities/project evidence 25, tools/technical evidence
20, education/eligibility evidence 10, clarity 5. Award points only for evidence visible in the resume.
"""

def extract_resume(upload):
    if upload is None:
        return ""
    name = upload.name.lower()
    raw = upload.getvalue()
    if name.endswith(".txt"):
        return raw.decode("utf-8", errors="ignore")
    if name.endswith(".pdf"):
        reader = PdfReader(io.BytesIO(raw))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    raise ValueError("Please upload a PDF or TXT resume.")

def tokens(text):
    return set(re.findall(r"[a-zA-Z][a-zA-Z0-9+#.]{1,}", text.lower()))

def analyse(resume, jd):
    if len(resume.strip()) < 30 or len(jd.strip()) < 30:
        raise ValueError("Please provide a resume and job description with at least 30 characters each.")
    r, j = tokens(resume), tokens(jd)
    stop = {"with","this","that","from","your","have","will","able","work","role","team","the","and","for","are","you","our","their","using","into","about","years","year","job","description","candidate","skills","responsibilities","required","preferred"}
    req = sorted(t for t in (j-stop) if len(t) > 2)
    matched = [t for t in req if t in r]
    missing = [t for t in req if t not in r]
    coverage = len(matched)/max(1,len(req))
    score = round(coverage*70 + min(20, len([x for x in ["project","internship","experience","coursework","developed","built"] if x in r])*3) + (10 if len(resume)>500 else 4))
    return {
        "score": min(100,score), "matched":matched[:25], "missing":missing[:25],
        "matched_count":len(matched), "compared_count":len(req),
        "improvements":[
            "Add a truthful project or coursework example for each important skill you can substantiate.",
            "Use job-description terminology only when it accurately describes your experience.",
            "Quantify outcomes only when you have real measurements; never invent numbers.",
            "Move the strongest relevant evidence into the top half of your resume."
        ]
    }

st.markdown('<div class="hero"><div class="smallcap">YOUR NEXT OPPORTUNITY, MORE CLEARLY</div><h1>AI Career<span>Compass</span></h1><p>Compare your resume with a job description. Find evidenced matches, gaps and practical next steps.</p></div>', unsafe_allow_html=True)
st.caption("Prompt Syndicate · SCSE4041 · Milestone 2")

with st.form("career_form"):
    left, right = st.columns(2)
    with left:
        st.subheader("01 / Your resume")
        resume_text = st.text_area("Paste resume text", height=250, placeholder="Paste your resume content here...")
        resume_file = st.file_uploader("Or upload a resume (PDF/TXT)", type=["pdf","txt"])
    with right:
        st.subheader("02 / Job description")
        jd_text = st.text_area("Paste job description", height=330, placeholder="Paste the internship/job requirements and responsibilities...")
    submitted = st.form_submit_button("Analyse my match", type="primary", use_container_width=True)

if submitted:
    try:
        resume = extract_resume(resume_file) if resume_file else resume_text
        result = analyse(resume, jd_text)
        st.divider()
        st.subheader("Your match snapshot")
        c1,c2,c3 = st.columns(3)
        c1.metric("Indicative keyword match", f"{result['score']}/100")
        c2.metric("Matching terms", result["matched_count"])
        c3.metric("Compared terms", result["compared_count"])
        a,b = st.columns(2)
        with a:
            st.markdown("### Evidenced matching terms")
            if result["matched"]:
                st.markdown(" ".join(f'<span class="pill">{x}</span>' for x in result["matched"]), unsafe_allow_html=True)
            else:
                st.info("No clear keyword matches found.")
        with b:
            st.markdown("### Terms not evidenced")
            if result["missing"]:
                st.write(", ".join(result["missing"]))
            else:
                st.success("No unmatched terms in this baseline comparison.")
        st.markdown("### Suggested next steps")
        for item in result["improvements"]:
            st.write("• " + item)
        st.markdown("### Truthful bullet-point framework")
        st.info("Use only if accurate: Applied [skill/tool] to [specific task] in [project/coursework], producing [verifiable outcome].")
        st.markdown('<div class="warn">This prototype currently uses an explainable keyword-overlap baseline. It is not a live generative-AI judgement. A missing keyword does not prove you lack that skill, and this score is not a hiring decision.</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(str(e))

with st.expander("About the prompt design"):
    st.write("The designed master prompt emphasizes evidence-only analysis, no invented qualifications or metrics, transparent scoring, and truthful improvement suggestions.")
    st.code(MASTER_PROMPT, language="text")

st.divider()
st.caption("AI CareerCompass · Prompt Syndicate | Prototype for educational use")
