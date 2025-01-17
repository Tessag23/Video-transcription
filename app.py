from flask import Flask, request, render_template
import whisper
import os

app = Flask(__name__)

# Load the Whisper model (you can use 'base' or 'small' for faster results)
model = whisper.load_model("base")

# Create a folder to store uploaded files
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Set up the upload folder in the app config
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Home page route
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle file upload and transcription
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file', 400
    
    # Save the uploaded file
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    
    # Transcribe the video file using Whisper
    try:
        result = model.transcribe(filepath)
        return render_template('index.html', transcription=result["text"])
    except Exception as e:
        return f'Error processing the file: {str(e)}', 500

if __name__ == '__main__':
    app.run(debug=True) 