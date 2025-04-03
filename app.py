from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os
import fitz  # PyMuPDF
import docx
from classify import classify_text

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text(filepath):
    ext = filepath.rsplit('.', 1)[1].lower()
    if ext == 'pdf':
        text = ""
        with fitz.open(filepath) as doc:
            for page in doc:
                text += page.get_text()
        return text
    elif ext == 'docx':
        doc = docx.Document(filepath)
        return '\n'.join([p.text for p in doc.paragraphs])
    else:
        return ""

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Extract and classify
            text = extract_text(filepath)
            classification = classify_text(text)
            return render_template('result.html', category=classification)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
