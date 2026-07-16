import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from pypdf import PdfReader


load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError ("api error")

client = Groq(api_key=my_api_key)
model = "llama-3.3-70b-versatile"

# pdf reader
reader = PdfReader("kumargauravkg.pdf")

#Read all text
text = ""
for page in reader.pages:
    page_text = page.extract_text()
    # if any page contain none value then skip that page
    if page_text:
        text += page_text

requirement = {
    "skill": ["python", "mysql", "Rest API", "Javascript"],
    "experience": 0
}

from pydantic import BaseModel
class ResumeMatch(BaseModel):
    name: str
    skills: list[str]
    experience: int
    score: int
    strengths: list[str]
    weaknesses: list[str]
    recommendation: str

schema = ResumeMatch.model_json_schema()

resonse_format = {
    "type": "json_object"
}

system_prompt = f"""
You are an expert technical recruiter.

Analyze the candidate's resume

and extract information based on this {schema}

Then compare the candidate against job requirements.

Finally provide exact these keys in the output JSON:

    "name": "",
    "skills": [],
    "experience": 0,
    "score": 0,
    "missing_skills": [],
    "strengths": [],
    "weaknesses": [],
    "recommendation": ""

Respond ONLY in JSON.
""" 

system_message = {
    "role":"system",
    "content": system_prompt
}

prompt = f"Job Requirements: {requirement} Candidate Resume: {text}"

message = {
    "role":"user",
    "content": prompt
}

messages = [system_message, message]

response = client.chat.completions.create(
    model=model,
    messages=messages,
    response_format=resonse_format
)

answer = response.choices[0].message.content
print(answer)

import json
raw_json = answer
data_file = json.loads(raw_json)
requirement = ResumeMatch(**data_file)

print(f"Candidate Name: {requirement.name}")
print(f"Matching Score: {requirement.score}")
print(f"Recommendation: {requirement.recommendation}")