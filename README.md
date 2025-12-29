# 🔒 AI Security Report Assistant

An intelligent security analysis tool that leverages AI to analyze vulnerability findings and generate actionable security reports. The application provides risk summaries, severity assessments, and detailed remediation steps for identified security vulnerabilities.

## ✨ Features

- **AI-Powered Analysis**: Uses OpenAI's GPT models to analyze security vulnerabilities
- **Risk Assessment**: Generates concise risk summaries for each finding
- **Severity Classification**: Automatically assigns severity levels (Low, Medium, High, Critical)
- **Remediation Guidance**: Provides specific, actionable remediation steps
- **User-Friendly Interface**: Clean, professional web UI for easy interaction
- **RESTful API**: FastAPI backend with comprehensive error handling

## 🏗️ Architecture

### Backend
- **Framework**: FastAPI (Python)
- **AI Integration**: OpenAI API (GPT-3.5-turbo)
- **API Endpoint**: `/process` - Accepts vulnerability text and returns AI-generated analysis

### Frontend
- **Technology**: HTML, CSS, JavaScript
- **Features**: 
  - Textarea for vulnerability input
  - Real-time analysis with loading indicators
  - Dynamic result display with color-coded severity badges
  - Responsive design

### Directory Structure
```
ai-security-report-assistant/
├── backend/
│   └── main.py           # FastAPI application and endpoints
├── frontend/
│   └── index.html        # Web UI
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variable template
├── .gitignore            # Git ignore patterns
└── README.md             # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/mohsena0204-lgtm/ai-security-report-assistant.git
   cd ai-security-report-assistant
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your OpenAI API key
   # OPENAI_API_KEY=your_actual_api_key_here
   ```

### Running the Application

1. **Start the backend server**
   ```bash
   python backend/main.py
   ```
   
   The server will start on `http://localhost:8000`

2. **Access the application**
   
   Open your web browser and navigate to:
   ```
   http://localhost:8000/static/index.html
   ```

3. **Using the application**
   - Enter vulnerability details in the text area
   - Click "Analyze Vulnerability" button
   - View the AI-generated analysis including:
     - Risk summary
     - Severity level
     - Remediation steps

## 📡 API Documentation

### Endpoint: `POST /process`

Processes vulnerability findings and returns AI-generated analysis.

**Request Body:**
```json
{
  "vulnerability_text": "SQL Injection vulnerability found in login form"
}
```

**Response:**
```json
{
  "risk_summary": "This SQL injection vulnerability allows attackers to manipulate database queries...",
  "severity": "High",
  "remediation_steps": [
    "Use parameterized queries or prepared statements",
    "Implement input validation and sanitization",
    "Apply principle of least privilege to database accounts",
    "Enable database query logging and monitoring",
    "Conduct regular security code reviews"
  ]
}
```

**Status Codes:**
- `200 OK`: Successful analysis
- `400 Bad Request`: Invalid input (empty text)
- `500 Internal Server Error`: API key not configured or processing error

### Interactive API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Yes | - |
| `ALLOWED_ORIGINS` | Comma-separated list of allowed CORS origins | No | `http://localhost:8000,http://localhost:8080` |

**Note:** For production deployments, set `ALLOWED_ORIGINS` to your actual domain(s) to enhance security.

## 🧪 Example Vulnerability Inputs

Try these example inputs to test the application:

1. **SQL Injection**
   ```
   SQL Injection vulnerability in the user login form allows attackers to bypass authentication by entering malicious SQL code in the username field.
   ```

2. **Cross-Site Scripting (XSS)**
   ```
   Reflected XSS vulnerability in the search parameter allows attackers to inject malicious scripts that execute in users' browsers.
   ```

3. **Exposed API Keys**
   ```
   API keys and secrets are hardcoded in the source code and committed to the public repository, potentially exposing sensitive credentials.
   ```

## 🛠️ Development

### Running in Development Mode

For development with auto-reload:

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Code Structure

**Backend (backend/main.py)**
- FastAPI application setup
- CORS middleware configuration
- Static file serving for frontend
- `/process` endpoint implementation
- OpenAI API integration
- Error handling and validation

**Frontend (frontend/index.html)**
- Responsive UI with gradient design
- Form handling and validation
- Asynchronous API calls
- Dynamic result rendering
- Loading states and error handling

## 🔒 Security Considerations

- API keys are stored in environment variables, not in code
- Input validation prevents empty submissions
- Error messages don't expose sensitive information
- CORS origins can be configured via environment variables for production
- Default CORS settings use localhost only (safe for development)
- httpx version pinned for compatibility and security

## 📦 Dependencies

- **fastapi**: Modern web framework for building APIs
- **uvicorn**: ASGI server for running FastAPI
- **openai**: Official OpenAI Python client
- **python-dotenv**: Environment variable management
- **pydantic**: Data validation using Python type annotations

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available for educational purposes.

## 🙏 Acknowledgments

- OpenAI for providing the GPT API
- FastAPI for the excellent web framework
- The security community for vulnerability classification standards
