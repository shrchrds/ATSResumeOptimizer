# 🧠 ATS Resume Optimizer with CrewAI and Groq

This project leverages the power of CrewAI's multi-agent framework and Groq's high-speed LLMs to create an intelligent ATS (Applicant Tracking System) resume optimizer.

Users can upload their resume, provide a target job title and description, and the AI crew will automatically:
1.  Parse and clean the resume text.
2.  Rewrite the resume to be highly optimized for the target job.
3.  Refine the bullet points with quantifiable metrics and strong action verbs.
4.  Provide a final ATS score and actionable recommendations for improvement.

The entire application is wrapped in a user-friendly Streamlit web interface.

## ✨ Features

-   **File Upload**: Accepts `.pdf`, `.docx`, and `.txt` resume files.
-   **Resume Cleaning**: Extracts clean, workable text from uploaded files, removing formatting artifacts.
-   **ATS Optimization**: Strategically rewrites the resume to align with keywords and themes from the job description.
-   **Bullet Point Refinement**: Enhances work experience bullet points to be more impactful by adding metrics and powerful verbs.
-   **ATS Evaluation**: Provides a final score (0-100) and a structured JSON output with strengths, weaknesses, and suggestions.
-   **Downloadable Results**: Allows users to download the cleaned, rewritten, and final versions of their resume.

## 🛠️ Tech Stack

-   **Framework**: Streamlit (for the web UI)
-   **AI Orchestration**: CrewAI
-   **LLM Provider**: Groq (using the Llama3 8B model via an OpenAI-compatible endpoint)
-   **Language**: Python
-   **Core Libraries**: `langchain-openai`, `python-dotenv`, `pypdf`, `python-docx`

## ⚙️ How It Works

The application uses a sequential crew of four specialized AI agents, each with a distinct role:

1.  **Resume Parsing Specialist**: This agent's only job is to take the raw text extracted from the resume file and clean it into a structured, plain-text format.
2.  **ATS Optimization Writer**: This agent receives the cleaned resume and the job description. It rewrites the entire resume to maximize its ATS score by aligning it with the job's requirements.
3.  **Bullet Point Refiner**: This agent takes the rewritten resume and focuses exclusively on improving the work experience bullet points, making them more powerful and metric-driven.
4.  **ATS Evaluator**: The final agent reviews the refined resume against the job description and generates a detailed evaluation report and an overall score.

## 📁 Project Structure

```
.
├── file_tools/
│   ├── __init__.py
│   └── file_loader.py
├── .env
├── agents.py
├── crew.py
├── requirements.txt
├── streamlit_app.py
├── tasks.py
└── utils.py
```

## 🚀 Setup and Installation

Follow these steps to get the application running locally.

### 1. Clone the Repository

```bash
git clone https://github.com/shrchrds/ATSResumeOptimizer.git
cd ATSResumeOptimizer
```

### 2. Create a Virtual Environment

It's highly recommended to use a virtual environment to manage dependencies.

```bash
# For Mac/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies

Create a `requirements.txt` file in the root directory with the following content:

```txt
crewai
streamlit
python-dotenv
langchain-openai
pypdf
python-docx
```

Then, install the libraries from the file:

```bash
pip install -r requirements.txt
```

### 4. Configure Your API Key

Create a file named `.env` in the root of the project directory and add your Groq API key.

```
GROQ_API_KEY="gsk_YourActualGroqApiKeyHere..."
```

## ▶️ Running the Application

Once the setup is complete, you can launch the Streamlit web application with a single command:

```bash
streamlit run app.py
```

The application will open in your web browser.

## ⚠️ Important Note on Configuration

This project uses a specific environment variable setup in `streamlit_app.py` to work around a known bug in some versions of the `crewai` library. The library can incorrectly demand an `OPENAI_API_KEY` even when a different LLM provider is specified.

The code in `streamlit_app.py` resolves this by:

```python
# Sets the API key for the OpenAI client to your Groq key
os.environ["OPENAI_API_KEY"] = os.getenv("GROQ_API_KEY")

# Points the client to Groq's OpenAI-compatible server
os.environ["OPENAI_API_BASE"] = "https://api.groq.com/openai/v1"

# Sets the default model name
os.environ["OPENAI_MODEL_NAME"] = "llama-3.3-70b-versatile"
```

This setup "tricks" CrewAI into thinking it's using OpenAI, while all API calls are correctly and securely routed to Groq's servers with the proper authentication. **No data is sent to OpenAI.**

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.