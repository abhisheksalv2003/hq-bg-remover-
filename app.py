from flask import Flask, render_template, request
from rembg import remove
from PIL import Image
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
OUTPUT_FOLDER = 'static/outputs'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    filename = None
    if request.method == 'POST':
        image = request.files['image']
        if image:
            input_path = os.path.join(UPLOAD_FOLDER, image.filename)
            image.save(input_path)

            output_filename = image.filename.rsplit('.', 1)[0] + '_no_bg.png'
            output_path = os.path.join(OUTPUT_FOLDER, output_filename)

            with Image.open(input_path) as img:
                no_bg = remove(img)
                no_bg.save(output_path)

            filename = output_filename

    return render_template('index.html', filename=filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
