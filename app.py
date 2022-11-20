from flask import Flask, render_template, request
from src.ANPR.pipeline.prediction_pipeline import OCR
from werkzeug.datastructures import FileStorage
import os, shutil
from src.ANPR.constants import *
# webserver gateway interface
app = Flask(__name__)

BASE_PATH = os.getcwd()
UPLOAD_PATH = os.path.join(BASE_PATH, 'static','upload')


@app.route('/', methods=['POST', 'GET'])
def land():
    return render_template('landing_page.html')

@app.route('/index', methods=['POST', 'GET'])
def index():
   
   
    if request.method == 'POST':
        
        upload_file = request.files['fileup']
        filename = upload_file.filename
        upload_img_path = os.path.join(os.getcwd(), STATIC_DIR, UPLOAD_SUB_DIR)
        shutil.rmtree(upload_img_path)
        os.makedirs(upload_img_path, exist_ok=True)
        upload_img_path = os.path.join(os.getcwd(), STATIC_DIR, UPLOAD_SUB_DIR,filename)
        upload_file.save(upload_img_path)
        text = OCR(upload_img_path, filename)

        return render_template('index.html', upload=True, upload_image=filename, text=text)

    return render_template('index.html', upload=False)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,debug=True)