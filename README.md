# Resume Analyzer Web Application

A Flask-based web application that analyzes resumes against job descriptions and skills.

## Features
- Upload multiple resumes (PDF/DOCX)
- Enter job description and key skills
- View match percentages in interactive charts
- Download original resumes
- Responsive design works on all devices

## Installation
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Download NLTK data:
   ```python
   import nltk
   nltk.download('stopwords')
   nltk.download('punkt')
   ```

## Running the Application
```bash
python app.py
```
Then open http://localhost:5000 in your browser.

## File Structure
```
.
├── app.py                 # Main Flask application
├── resume_analyzer.py     # Resume analysis logic
├── requirements.txt       # Python dependencies
├── static/
│   ├── css/styles.css     # Custom styles
│   ├── js/                # JavaScript files
│   └── uploads/           # Resume storage
└── templates/
    ├── base.html          # Base template
    ├── index.html         # Upload form
    └── results.html       # Results display
```

## Requirements
- Python 3.7+
- See requirements.txt for package dependencies

## Screenshots
![Upload Page](screenshots/upload.png)
![Results Page](screenshots/results.png)