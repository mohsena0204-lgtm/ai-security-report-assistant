from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import google.generativeai as genai
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

# Get Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


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
    Process vulnerability finding and return AI-generated analysis using Google Gemini.
    
    Args:
        input_data: VulnerabilityInput containing the vulnerability text
        
    Returns:
        AnalysisResult with risk summary, severity, and remediation steps
    """
    if not input_data.vulnerability_text.strip():
        raise HTTPException(status_code=400, detail="Vulnerability text cannot be empty")
    
    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=500, 
            detail="Gemini API key not configured. Please set GEMINI_API_KEY environment variable."
        )
    
    try:
        # Create prompt for Gemini
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

        # Initialize Gemini model (using Gemini 1.5 Flash for optimal performance)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Configure generation parameters
        generation_config = genai.GenerationConfig(
            temperature=0.7,
            max_output_tokens=800,
        )
        
        # Generate response
        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )
        
        # Extract response text
        response_text = response.text.strip()
        
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
