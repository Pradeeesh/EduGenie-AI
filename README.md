# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a FastAPI + HTML/CSS educational assistant based on the supplied project documentation. It supports:

- Question answering (`/qa`)
- Topic explanation (`/explain`)
- Three-question MCQ quiz generation (`/quiz`)
- Text summarization (`/summarize`)
- Beginner-to-advanced learning paths (`/learn/recommendations`)

The original documentation describes Gemini 1.5 Pro for Q&A, quiz, summary and learning-path generation and LaMini-Flan-T5-783M for explanations. This implementation preserves those functional roles but uses the current `google-genai` SDK and a configurable current Gemini model. The explanation backend can be Gemini by default or the documented LaMini model when `EXPLAINER_BACKEND=local`.

## Project structure

```text
EduGenie/
├── main.py
├── config.py
├── gemini_client.py
├── schemas.py
├── explanation_module.py
├── qna.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── run.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
├── static/
│   ├── app.js
│   └── style.css
└── tests/
    └── test_app.py
```

## 1. Prerequisites

Install Python 3.10 or newer. The project uses FastAPI, Uvicorn, Jinja2 and Google Gemini through the `google-genai` Python SDK.

## 2. Open in VS Code

Open the `EduGenie` folder in VS Code.

Create a virtual environment:

### Windows PowerShell

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If `py` is unavailable:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

> `torch` and `transformers` are included because the project supports the documented local LaMini explainer. For the default Gemini explainer, these packages are not used at runtime.

## 4. Configure Gemini

Copy `.env.example` to `.env` and put your Gemini API key in:

```env
GEMINI_API_KEY=your_real_key_here
```

Keep `.env` private and do not commit it to Git.

The default model is configurable:

```env
GEMINI_MODEL=gemini-2.5-flash
```

## 5. Run the application

Recommended:

```bash
python run.py
```

Or directly:

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

## 6. Test the API

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Question:

```bash
curl -X POST http://127.0.0.1:8000/qa ^
  -H "Content-Type: application/json" ^
  -d "{\"question\":\"What is photosynthesis?\"}"
```

On macOS/Linux, use `\\` instead of `^` for multiline shell commands, or put the JSON on one line.

Quiz:

```bash
curl -X POST http://127.0.0.1:8000/quiz \
  -H "Content-Type: application/json" \
  -d '{"text":"Photosynthesis is the process by which green plants use light energy to make food from carbon dioxide and water.","question_count":3}'
```

## 7. Run automated tests

```bash
pytest -q
```

These tests cover the homepage, health endpoint and basic request validation without making Gemini API calls.

## 8. API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Web application |
| GET | `/health` | Application/API status |
| POST | `/qa` | Educational Q&A |
| POST | `/explain` | Concept explanation |
| POST | `/quiz` | MCQ generation |
| POST | `/summarize` | Educational summarization |
| POST | `/learn/recommendations` | Learning path |

Interactive API documentation is also available at `/docs` while the server is running.

## 9. Optional local LaMini explainer

The supplied documentation identifies `MBZUAI/LaMini-Flan-T5-783M` as the local model for concept explanations. To use it:

```env
EXPLAINER_BACKEND=local
LOCAL_EXPLAINER_MODEL=MBZUAI/LaMini-Flan-T5-783M
```

On the first `/explain` request, Transformers downloads the model. This can require substantial disk space and CPU/RAM. If loading the local model fails, the implementation falls back to Gemini.

## 10. Troubleshooting

### "GEMINI_API_KEY is not configured"

Make sure `.env` exists in the project root and contains a valid key. Restart Uvicorn after changing `.env`.

### Gemini model error

Set `GEMINI_MODEL` to a model currently available to your API key. The model name is intentionally configurable so the application does not hard-code a retired model.

### PowerShell activation is blocked

If your PowerShell execution policy prevents activation, use Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

### Port already in use

Change the `.env` value:

```env
PORT=8001
```

Then open `http://127.0.0.1:8001`.
