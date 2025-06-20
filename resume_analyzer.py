import os
import re
import PyPDF2
import docx
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from collections import Counter
from typing import Dict, List

nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))

def extract_text_pdf(filepath: str) -> str:
    """Extract text from PDF file"""
    text = ""
    with open(filepath, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + " "
    return text

def extract_text_docx(filepath: str) -> str:
    """Extract text from DOCX file"""
    doc = docx.Document(filepath)
    return " ".join([para.text for para in doc.paragraphs])

def process_text(text: str) -> str:
    """Clean and tokenize text"""
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    words = nltk.word_tokenize(text.lower())
    return ' '.join([word for word in words if word not in stop_words])

def extract_summary(text: str) -> str:
    """Extract summary section from resume text"""
    keywords = ["summary", "objective", "career objective", "profile"]
    lines = text.split("\n")
    for i, line in enumerate(lines):
        for keyword in keywords:
            if keyword in line.lower():
                return ' '.join(lines[i:i+3])
    return ""

def extract_sections(text: str) -> Dict[str, str]:
    """Extract key sections from resume"""
    sections = {
        "experience": [],
        "skills": [],
        "certifications": [],
        "projects": []
    }
    titles = {
        "experience": ["experience", "work history", "employment"],
        "skills": ["skills", "technical skills", "key skills"],
        "certifications": ["certifications", "certificates", "credentials"],
        "projects": ["projects", "research", "publications"]
    }
    
    lines = text.split("\n")
    current = None
    
    for line in lines:
        line_lower = line.lower()
        for section, keywords in titles.items():
            if any(keyword in line_lower for keyword in keywords):
                current = section
                break
        if current and line.strip():
            sections[current].append(line)
    
    return {k: ' '.join(v) for k, v in sections.items()}

def process_resumes(filenames: List[str], job_desc: str, keywords: List[str]) -> Dict[str, float]:
    """Process multiple resumes and return match scores"""
    results = {}
    job_desc_clean = process_text(job_desc)
    keywords_clean = [process_text(k.strip()) for k in keywords if k.strip()]
    
    for filename in filenames:
        filepath = os.path.join('static/uploads', filename)
        
        try:
            if filename.endswith(".pdf"):
                text = extract_text_pdf(filepath)
            elif filename.endswith(".docx"):
                text = extract_text_docx(filepath)
            else:
                continue
                
            text_clean = process_text(text)
            summary = extract_summary(text_clean)
            sections = extract_sections(text_clean)
            
            # Calculate TF-IDF similarity
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform([job_desc_clean, summary])
            job_score = (tfidf_matrix * tfidf_matrix.T).toarray()[0, 1] * 100
            
            # Calculate keyword score
            keyword_score = 0
            for keyword in keywords_clean:
                for section, content in sections.items():
                    if keyword in content:
                        if section == "experience":
                            keyword_score += 30
                        elif section == "skills":
                            keyword_score += 20
                        elif section == "certifications":
                            keyword_score += 15
                        elif section == "projects":
                            keyword_score += 10
            
            total_score = min(100, job_score + keyword_score)
            results[filename] = round(total_score, 2)
            
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
            results[filename] = 0.0
    
    return results