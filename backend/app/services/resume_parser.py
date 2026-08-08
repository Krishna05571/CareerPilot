from google import genai
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Initialize client (NEW SDK)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def parse_resume_with_ai(text: str):
    try:
        # models = client.models.list()

        # for m in models:
        #     print(m.name)

        prompt = f"""
You are an AI Resume Analyzer.

Analyze the following resume text and extract structured, clean, and professional information.

Resume:
{text}

IMPORTANT INSTRUCTIONS:
- Return ONLY valid JSON (no explanation, no markdown)
- Do not include ```json or ``` blocks
- Ensure all fields are present (use empty list [] if not found)
- Keep output clean and consistent
- Normalize skill names (e.g., "js" → "JavaScript")
- Remove duplicates in skills
- Capitalize names properly

Return JSON in this EXACT format:

{{
  "name": "",
  "email": "",
  "skills": [],
  "education": [],
  "experience": [],
  
  "resume_score": 0,

  "strengths": [],
  "weaknesses": [],
  "improvement_suggestions": [],

  "suggested_roles": [
    {{
      "role": "",
      "reason": ""
    }}
  ],

  "skill_gap_analysis": [
    {{
      "target_role": "",
      "missing_skills": []
    }}
  ]
}}
"""

        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )

        # Convert response to JSON safely
        raw_text = response.text.strip()

        # Sometimes Gemini returns ```json ... ```
        if raw_text.startswith("```"):
            raw_text = raw_text.replace("```json", "").replace("```", "").strip()

        return json.loads(raw_text)

    except Exception as e:
        return {"error": str(e)}