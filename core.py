import re

STOP = {"with","this","that","from","your","have","will","able","work","role","team","the","and","for","are","you","our","their","using","into","about","years","year","job","description","candidate","skills","responsibilities","required","preferred"}

def tokens(text):
    return set(re.findall(r"[a-zA-Z][a-zA-Z0-9+#.]{1,}", text.lower()))

def analyse(resume, jd):
    if len(resume.strip()) < 30 or len(jd.strip()) < 30:
        raise ValueError("Please provide a resume and job description with at least 30 characters each.")
    r, j = tokens(resume), tokens(jd)
    req = sorted(t for t in (j-STOP) if len(t) > 2)
    matched = [t for t in req if t in r]
    missing = [t for t in req if t not in r]
    coverage = len(matched)/max(1,len(req))
    score = round(coverage*70 + min(20, len([x for x in ["project","internship","experience","coursework","developed","built"] if x in r])*3) + (10 if len(resume)>500 else 4))
    score = min(100, score)
    return {"score":score,"matched":matched[:25],"missing":missing[:25],"matched_count":len(matched),"compared_count":len(req),"note":"This prototype uses an explainable keyword-overlap baseline. It is not a hiring decision and does not prove that an unlisted skill is absent.","improvements":["Add a truthful project or coursework example for each important skill you can substantiate.","Mirror relevant job-description terminology only when it accurately describes your experience.","Quantify outcomes only when you have real measurements; never invent numbers.","Move the strongest relevant evidence into the top half of the resume."],"bullet":"Use this structure only if accurate: ‘Applied [skill/tool] to [specific task] in [project/coursework], producing [verifiable outcome].’"}
