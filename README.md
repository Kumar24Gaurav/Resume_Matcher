# AI Resume Matcher

An AI-powered tool that analyzes a candidate's resume (PDF) against a set of job requirements and returns a structured evaluation — extracted skills, experience, a match score, strengths, weaknesses, and a hiring recommendation.

Built using [Groq](https://groq.com/) (Llama 3.3 70B Versatile) for fast LLM inference and `pydantic` for structured, validated output.

## Features

- 📄 **PDF Parsing** — Extracts text from resume PDFs using `pypdf`.
- 🤖 **LLM-Powered Analysis** — Uses Groq's `llama-3.3-70b-versatile` model to read the resume and compare it against defined job requirements.
- ✅ **Structured Output** — Enforces a consistent JSON schema (name, skills, experience, score, strengths, weaknesses, recommendation) via a `pydantic` model.
- 🎯 **Job Matching** — Scores candidates against a configurable list of required skills and experience level.

## How It Works

1. The script loads a resume PDF and extracts all readable text.
2. A job requirement dictionary (skills + minimum experience) is defined in code.
3. A system prompt instructs the LLM to act as an expert technical recruiter, analyze the resume, and compare it to the job requirements.
4. The Groq API is called with `response_format={"type": "json_object"}` to force valid JSON output.
5. The JSON response is parsed and validated against the `ResumeMatch` pydantic model.
6. Key results (name, score, recommendation) are printed to the console.

## Requirements

- Python 3.11
- A [Groq API key](https://console.groq.com/keys)

### Dependencies

```
groq
pypdf
python-dotenv
pydantic
```

Install them with:

```bash
pip install groq pypdf python-dotenv pydantic
```

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/Kumar24Gaurav/Resume_Screening.git
   cd <your-repo>
   ```

2. Create a `.env` file in the project root and add your Groq API key:

   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

3. Place the candidate's resume PDF in the project directory (update the filename in the script if needed, e.g. `kumargauravkg.pdf`).

## Usage

Run the script:

```bash
python main.py
```

### Customizing Job Requirements

Edit the `requirement` dictionary in the script to match the role you're hiring for:

```python
requirement = {
    "skill": ["python", "mysql", "Rest API", "Javascript"],
    "experience": 0
}
```

## Example Output

```
{
  "name": "Kumar Gaurav",
   "skills": ["Python", "JavaScript", "MySQL", "Rest API"],
   "experience": 4,
   "score": 8,
   "missing_skills": [],
   "strengths": ["Python development", "RESTful API design", "Full stack development"],
   "weaknesses": ["Lack of experience with large-scale projects"],
   "recommendation": "The candidate has the required skills and some experience with Python, JavaScript, MySQL, and Rest API, making him a good fit for the job."
}
Candidate Name: Kumar Gaurav
Matching Score: 8
Recommendation: The candidate has the required skills and some experience with Python, JavaScript, MySQL, and Rest API, making him a good fit for the job.
```

The full structured result includes:

| Field         | Description                                      |
|---------------|---------------------------------------------------|
| `name`        | Candidate's full name                              |
| `skills`      | Skills extracted from the resume                   |
| `experience`  | Years of experience (as inferred by the model)      |
| `score`       | Overall match score against job requirements        |
| `strengths`   | Notable strengths relative to the role              |
| `weaknesses`  | Gaps or weaknesses relative to the role              |
| `recommendation` | Final hiring recommendation                       |

## Project Structure

```
.
├── main.py              # Main script (resume parsing + LLM analysis)
├── kumargauravkg.pdf     # Example candidate resume (input)
├── .env                  # Environment variables (not committed)
└── README.md
```

## Notes

- The `.env` file should **never** be committed to version control. Add it to `.gitignore`.
- The model used (`llama-3.3-70b-versatile`) can be swapped for any other Groq-supported model.
- This is a simple, single-resume proof of concept — it can be extended to batch-process multiple resumes, add a web UI, or export results to a database/spreadsheet.
