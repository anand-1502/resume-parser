import os
import sys
from flask import Flask, request, render_template
from pypdf import PdfReader
import json
from resumeparser import extract_resume_info


# Add current directory to system path
sys.path.insert(0, os.path.abspath(os.getcwd()))

# Set upload folder path
UPLOAD_FOLDER = r"__DATA__"
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def home():
    """Render the main page."""
    return render_template('index.html')


@app.route("/upload", methods=["POST"])
def process_resume():
    """Handle the uploaded PDF, process it and return the result."""
    uploaded_file = request.files.get('pdf_doc')
    
    if uploaded_file:
        # Save the uploaded file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], "uploaded_resume.pdf")
        uploaded_file.save(file_path)
        
        # Extract text from the PDF file
        extracted_data = extract_text_from_pdf(file_path)
        
        # Parse the data using the resume extraction function
        parsed_data = extract_resume_info(extracted_data)

        return render_template('index.html', data=json.loads(parsed_data))
    else:
        return "No file uploaded", 400


def extract_text_from_pdf(pdf_path):
    """Extract text from the given PDF file."""
    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text()

    return text


if __name__ == "__main__":
    app.run(debug=True, port=8000)
