import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from src.audio import runModel, generateDataframe

UPLOAD_FOLDER = 'input'
ALLOWED_EXTENSIONS = {'mp3'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            to = filename
            return redirect(to)
    return '''
<!doctype html>
<html lang=“en”>
<center>
<head>
    <meta charset=“UTF-8">
    <meta name=“viewport” content=“width=device-width, initial-scale=1.0">
    <title>Neural network tells frogs' familia apart</title>
</head>
<body style="background-color:#ffffff">
<h1>What Does The Frog Say? 🐸</h1>
<h2>Upload a recording: </h2>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file style="height:40px; width:85px">
      <input type=submit value=Upload style="height:20px; width:80px">
    </form>
<img src="https://media1.tenor.com/images/92cbbf4aacb333461ec36fd39cfda856/tenor.gif?itemid=5275848"/>
</body>
<center>
</html>
'''

@app.route('/<audioname>', methods=['GET'])
def accent (audioname):
    path = f"input/{audioname}"
    gendf = generateDataframe(path)
    result = runModel(gendf) #To predict  
    return '''
<!DOCTYPE html>
<html lang=“en”>
<center>
<head>
    <meta charset=“UTF-8">
    <meta name=“viewport” content=“width=device-width, initial-scale=1.0">
    <title>Neural network tells accents apart</title>
</head>
<body style="background-color:#ffffff">
<h1>What Does The Frog Say? 🐸</h1>
<img src="https://media1.tenor.com/images/bf479bab06999b5a3935596a573ea00d/tenor.gif?itemid=14977671"/>
<h2>{result}</h2>
<form>
    <input type="button" value="Go back" onclick="history.back()">
</form>
</body>
<center>
</html>
'''.format(result=result)

app.run('0.0.0.0', port=3000, debug=True, threaded=False) #http://0.0.0.0:3000/