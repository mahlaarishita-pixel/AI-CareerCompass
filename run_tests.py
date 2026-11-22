import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from core import analyse

cases = [
("T01 normal exact matches", "Python SQL data analysis academic project", "Data science intern Python SQL machine learning", lambda r: "python" in r["matched"] and "sql" in r["matched"]),
("T02 ML term match", "Python SQL machine learning and data visualization project", "Intern needs Python SQL machine learning data visualization", lambda r: "machine" in r["matched"] or "learning" in r["matched"]),
("T03 coursework evidence", "Completed data analysis coursework using Excel and Python", "Intern role requires data analysis Excel Python coursework", lambda r: r["score"] >= 0),
("T04 long resume", "Python SQL " + "data analytics project coursework "*100, "Role needs Python SQL data analytics and project experience", lambda r: r["score"] >= 0),
("T05 long JD", "Python SQL machine learning statistics visualization cloud project", "Requirements: " + "Python SQL machine learning statistics visualization cloud analytics "*30, lambda r: r["compared_count"] > 0),
("T06 no overlap", "Studied literature and history with essay writing experience", "Data engineering role requires Python SQL cloud pipelines machine learning", lambda r: len(r["matched"]) == 0),
("T07 empty resume", "", "Data science internship requires Python and SQL skills", lambda r: False),
("T08 empty JD", "Python SQL data analysis experience and academic project work", "", lambda r: False),
("T09 both short", "short", "tiny", lambda r: False),
("T10 synonym limitation", "Created charts and visual reports for a class project", "Role requires data visualization and dashboard development", lambda r: "visualization" in r["missing"]),
("T11 private contact text", "Email private@example.com phone 1234567890 Python SQL project experience", "Role needs Python SQL and project experience", lambda r: "private" not in str(r)),
("T12 score bounded", "Python SQL machine learning project experience coursework developed built", "Python SQL machine learning project experience", lambda r: 0 <= r["score"] <= 100),
]
passed=0
for name,resume,jd,check in cases:
    try:
        result=analyse(resume,jd)
        ok=check(result)
        actual=f"accepted; score={result['score']}; matched={result['matched'][:5]}"
    except ValueError as e:
        ok=name in ("T07 empty resume","T08 empty JD","T09 both short")
        actual=f"validation error: {e}"
    print(("PASS" if ok else "FAIL"), name, "|", actual)
    passed += bool(ok)
print(f"RESULT: {passed}/{len(cases)} passed")
if passed != len(cases): sys.exit(1)
