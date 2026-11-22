import os, re, io
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from pypdf import PdfReader

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024
ALLOWED = {"pdf", "txt"}

MASTER_PROMPT = """You are AI CareerCompass, a careful resume-to-job-description reviewer.
Use ONLY facts explicitly present in the resume. Never invent skills, employers, projects,
metrics, dates, degrees, certifications, or experience. Distinguish evidence from inference.
Compare the resume with the job description and return:
1) a match score out of 100 with a transparent rubric,
2) evidenced matching skills,
3) required skills not evidenced in the resume (do not assume the candidate lacks them),
4) evidence gaps and improvement priorities,
5) truthful rewritten bullet suggestions using placeholders where facts are missing,
6) an action plan.
If the resume or job description is missing/too short, ask for the missing material rather
than fabricating an analysis. Do not expose private contact details in the report.
Score rubric: required skills evidence 40, responsibilities/project evidence 25,
tools/technical evidence 20, education/eligibility evidence 10, clarity 5.
Award points only for evidence visible in the supplied resume. Explain the score.
"""

def extract_text(file_storage):
    name = secure_filename(file_storage.filename or "")
    ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
    if ext not in ALLOWED:
        raise ValueError("Upload a PDF or TXT resume.")
    raw = file_storage.read()
    if ext == "txt":
        return raw.decode("utf-8", errors="ignore")
    reader = PdfReader(io.BytesIO(raw))
    return "\n".join(page.extract_text() or "" for page in reader.pages)

from core import analyse

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/analyse", methods=["POST"])
def analyse_route():
    try:
        jd = request.form.get("job_description", "")
        resume = request.form.get("resume_text", "")
        upload = request.files.get("resume_file")
        if upload and upload.filename:
            resume = extract_text(upload)
        result = analyse(resume, jd)
        return render_template("result.html", result=result, prompt=MASTER_PROMPT)
    except Exception as e:
        return render_template("index.html", error=str(e)), 400

@app.route("/health")
def health():
    return jsonify(status="ok", app="AI CareerCompass")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
