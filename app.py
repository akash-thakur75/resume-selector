from flask import Flask, render_template, request
import os
from PyPDF2 import PdfReader

app = Flask(__name__)

@app.route("/")
def home():
    return render_template(
        "index.html",
        best_resume=None,
        best_score=None,
        results=[],
        job_description=""
    )


@app.route("/analyze", methods=["POST"])
def analyze():

    try:
        job_desc = request.form.get("job_description", "").strip()

        if not job_desc:
            return render_template(
                "index.html",
                error="Please enter a Job Description",
                job_description=""
            )

        resume_folder = "resumes"

        if not os.path.exists(resume_folder):
            return render_template(
                "index.html",
                error="resumes folder not found!",
                job_description=job_desc
            )

        files = [f for f in os.listdir(resume_folder) if f.endswith(".pdf")]

        if len(files) == 0:
            return render_template(
                "index.html",
                error="No PDF resumes found inside resumes folder!",
                job_description=job_desc
            )

        jd_words = set(job_desc.lower().split())

        results = []
        best_resume = None
        best_score = -1

        for file in files:

            path = os.path.join(resume_folder, file)

            text = ""

            try:
                reader = PdfReader(path)

                for page in reader.pages:
                    page_text = page.extract_text()

                    if page_text:
                        text += page_text

            except Exception as pdf_error:
                print("PDF ERROR:", file, pdf_error)
                continue

            resume_words = set(text.lower().split())

            score = len(jd_words.intersection(resume_words))

            results.append((file, score))

            if score > best_score:
                best_score = score
                best_resume = file

        return render_template(
            "index.html",
            best_resume=best_resume,
            best_score=best_score,
            results=results,
            job_description=job_desc
        )

    except Exception as e:
        return render_template(
            "index.html",
            error=str(e),
            job_description=""
        )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)