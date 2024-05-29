from flask import *
import os
from werkzeug.utils import secure_filename
import label_image

import image_fuzzy_clustering as fem
import os
import secrets
from PIL import Image
from flask import url_for, current_app



def load_image(image):
    text = label_image.main(image)
    return text




def prepare_image(image, target):
    # if the image mode is not RGB, convert it
    if image.mode != "RGB":
        image = image.convert("RGB")

    # resize the input image and preprocess it
    image = image.resize(target)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = imagenet_utils.preprocess_input(image)

    # return the processed image
    return image




app = Flask(__name__)
model = None

UPLOAD_FOLDER = os.path.join(app.root_path ,'static','img')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
@app.route('/first')
def first():
    return render_template('first.html')

 
  
    
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/chart')
def chart():
    return render_template('chart.html')

@app.route('/upload')
def upload():
    return render_template('index1.html')

@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        i=request.form.get('cluster')
        f = request.files['file']
        fname, f_ext = os.path.splitext(f.filename)
        original_pic_path=save_img(f, f.filename)
        destname = 'em_img.jpg'
        fem.plot_cluster_img(original_pic_path,i)
    return render_template('success.html')

def save_img(img, filename):
    picture_path = os.path.join(current_app.root_path, 'static/images', filename)
    # output_size = (300, 300)
    i = Image.open(img)
    # i.thumbnail(output_size)
    i.save(picture_path)

    return picture_path



@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload1():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']
        file_path = secure_filename(f.filename)
        f.save(file_path)
        # Make prediction
   def predict_heart_attack_risk(age, bmi, sbp, dbp, hba1c, dr_severity):
    # Check if conditions fall under normal category
    if (dr_severity == "None" or dr_severity == "Low") and \
       age < 40 and \
       bmi < 25 and \
       sbp < 120 and \
       dbp < 80 and \
       hba1c < 5.7:
        return "Very Low Risk"

    # Check if conditions fall under mild risk category
    if (dr_severity == "None" or dr_severity == "Low") and \
       40 <= age <= 50 and \
       25 <= bmi <= 29.9 and \
       120 <= sbp <= 129 and \
       80 <= dbp <= 84 and \
       5.7 <= hba1c <= 6.4:
        return "Mild Risk"

    # Check if conditions fall under moderate risk category
    if dr_severity == "Low" and \
       50 <= age <= 60 and \
       30 <= bmi <= 34.9 and \
       130 <= sbp <= 139 and \
       85 <= dbp <= 89 and \
       6.5 <= hba1c <= 7.4:
        return "Moderate Risk"

    # Check if conditions fall under high risk category
    if (dr_severity == "Moderate" or dr_severity == "High") and \
       age > 60 and \
       bmi >= 35 and \
       sbp >= 140 and \
       dbp >= 90 and \
       hba1c >= 7.5:
        return "High Chance of Heart Attack"

    # If conditions don't fall under any specific category, return default
    return "No Risk, You are Healthy"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Extract input values from the form
    age = int(request.form['age'])
    sbp = int(request.form['sbp'])
    dbp = int(request.form['dbp'])
    bmi = float(request.form['bmi'])
    hba1c = float(request.form['hba1c'])
    dr_severity = request.form['dr_severity']
    # Handle the uploaded image (you need to implement this part)
    uploaded_image = request.files['file']
    # Perform prediction using the uploaded image and input values
    prediction_result = predict_heart_attack_risk(age, bmi, sbp, dbp, hba1c, dr_severity)
    # Return the prediction result
    return render_template('prediction_result.html', result=prediction_result)

if __name__ == '__main__':
    app.run(debug=True)