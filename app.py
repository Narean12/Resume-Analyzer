from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from resume_analyzer import process_resumes

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'resumes' not in request.files:
        return redirect(request.url)
    
    files = request.files.getlist('resumes')
    job_desc = request.form.get('job_description', '')
    keywords = request.form.get('keywords', '').split(',')

    # Process and save files
    filenames = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filenames.append(filename)

    # Analyze resumes
    results = process_resumes(filenames, job_desc, keywords)
    
    return render_template('results.html', results=results)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)