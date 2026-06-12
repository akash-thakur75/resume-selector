import os
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Read Job Description
with open("job_description.txt", "r", encoding="utf-8") as f:
    job_description = f.read()

resume_folder = "resumes"

resume_texts = []
resume_names = []

# Read all PDF resumes
for file in os.listdir(resume_folder):

    if file.endswith(".pdf"):

        path = os.path.join(resume_folder, file)

        try:
            reader = PdfReader(path)

            text = ""

            for page in reader.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text

            resume_texts.append(text)
            resume_names.append(file)

        except Exception as e:
            print(f"Error reading {file}: {e}")

# Check if resumes found
if len(resume_texts) == 0:
    print("No PDF resumes found in resumes folder.")
    exit()

# Create TF-IDF vectors
documents = [job_description] + resume_texts

vectorizer = TfidfVectorizer()

vectors = vectorizer.fit_transform(documents)

jd_vector = vectors[0]

best_score = 0
best_resume = ""

print("\nResume Matching Results\n")

for i in range(len(resume_texts)):

    score = cosine_similarity(
        jd_vector,
        vectors[i + 1]
    )[0][0]

    print(f"{resume_names[i]} --> Match Score: {score:.4f}")

    if score > best_score:
        best_score = score
        best_resume = resume_names[i]

print("\n========================")
print("BEST MATCHED RESUME")
print("========================")
print("Selected Resume :", best_resume)
print("Match Score     :", round(best_score, 4))