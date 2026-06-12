from flask import Flask, render_template, request
import os
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer, util

app = Flask(__name__)

model = SentenceTransformer('all-MiniLM-L6-v2')


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    job_desc = request.form["job_description"]

    jd_embedding = model.encode(job_desc, convert_to_tensor=True)

    resume_folder = "resumes"

    best_resume = None
    best_score = 0
    results = []

    for file in os.listdir(resume_folder):
        if file.endswith(".pdf"):

            path = os.path.join(resume_folder, file)
            reader = PdfReader(path)

            text = ""
            for page in reader.pages:
                text += page.extract_text()

            resume_embedding = model.encode(text, convert_to_tensor=True)

            score = util.cos_sim(jd_embedding, resume_embedding).item()

            results.append((file, round(score, 4)))

            if score > best_score:
                best_score = score
                best_resume = file

    return render_template(
        "index.html",
        best_resume=best_resume,
        best_score=round(best_score, 4),
        results=results
    )


if __name__ == "__main__":
    app.run(debug=True)