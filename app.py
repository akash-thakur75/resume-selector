from flask import Flask, render_template, request
import os
from PyPDF2 import PdfReader

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    job_desc = request.form["job_description"].lower()

    resume_folder = "resumes"

    best_resume = None
    best_score = 0
    results = []

    jd_words = set(job_desc.split())

    for file in os.listdir(resume_folder):

        if file.endswith(".pdf"):

            path = os.path.join(resume_folder, file)

            reader = PdfReader(path)

            text = ""

            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted

            text = text.lower()

            resume_words = set(text.split())

            common_words = jd_words.intersection(resume_words)

            score = len(common_words)

            results.append((file, score))

            if score > best_score:
                best_score = score
                best_resume = file

    return render_template(
        "index.html",
        best_resume=best_resume,
        best_score=best_score,
        results=results
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)