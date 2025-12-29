from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import openai
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="AI Security Report Assistant")

# Get allowed origins from environment or use localhost for development
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:8000,http://localhost:8080").split(",")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for frontend
app.mount("/static", StaticFiles(directory="frontend", html=True), name="static")

# Get OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class VulnerabilityInput(BaseModel):
    """Model for vulnerability finding input"""
    vulnerability_text: str


class AnalysisResult(BaseModel):
    """Model for AI analysis result"""
    risk_summary: str
    severity: str
    remediation_steps: list[str]


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "AI Security Report Assistant API is running"}


@app.post("/process", response_model=AnalysisResult)
async def process_vulnerability(input_data: VulnerabilityInput):
    """
    Process vulnerability finding and return AI-generated analysis.
    
    Args:
        input_data: VulnerabilityInput containing the vulnerability text
        
    Returns:
        AnalysisResult with risk summary, severity, and remediation steps
    """
    if not input_data.vulnerability_text.strip():
        raise HTTPException(status_code=400, detail="Vulnerability text cannot be empty")
    
    if not OPENAI_API_KEY:
        raise HTTPException(
            status_code=500, 
            detail="OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
        )
    
    try:
        # Create prompt for OpenAI
        prompt = f"""You are a cybersecurity expert analyzing vulnerability findings. 
Analyze the following vulnerability finding and provide:

1. A concise risk summary (2-3 sentences)
2. A severity level (choose one: Low, Medium, High, Critical)
3. A list of 3-5 specific remediation steps

Vulnerability Finding:
{input_data.vulnerability_text}

Provide your response in the following JSON format:
{{
    "risk_summary": "your risk summary here",
    "severity": "Low/Medium/High/Critical",
    "remediation_steps": ["step 1", "step 2", "step 3", ...]
}}
"""

        # Call OpenAI API
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a cybersecurity expert. Always respond with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        # Extract and parse response
        response_text = response.choices[0].message.content.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        analysis_data = json.loads(response_text)
        
        # Validate severity
        severity = analysis_data.get("severity", "Medium").capitalize()
        if severity not in ["Low", "Medium", "High", "Critical"]:
            severity = "Medium"
        
        return AnalysisResult(
            risk_summary=analysis_data.get("risk_summary", "Analysis completed"),
            severity=severity,
            remediation_steps=analysis_data.get("remediation_steps", ["No specific steps provided"])
        )
        
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse AI response: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing vulnerability: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
