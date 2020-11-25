import flask
from flask import request
from flask import jsonify
import zipfile
import requests
from io import BytesIO
import json


app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['POST'])
def main():
    myZipFile = request.data
    headers = flask.request.headers
    respData = {}
    zipdata = BytesIO()
    zipdata.write(myZipFile)
    pID = headers.get('parent-id')
    print(pID)
    if zipfile.is_zipfile(zipdata):
        UnzippedFiles = []
        with zipfile.ZipFile(zipdata) as zip_ref:            
            for info in zip_ref.infolist():
                data = info.filename
                myHTML = zip_ref.read(data)
                UnzippedFiles.append(myHTML)
    response = app.response_class(
        response = UnzippedFiles,
        status = 200,
        mimetype = 'application/json'
    )
    return response

if __name__ == "__main__":
    app.run(debug=True)