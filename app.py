import flask
from flask import request
import zipfile
from io import BytesIO
import json
import csv


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
                myHTML = myHTML.decode("utf-8")                
                csv_reader = csv.reader(myHTML.split('\n'))
                for row in csv_reader:
                    if len(row) > 8 :
                        if row[6] == 'MO' :
                            UnzippedFiles.append(row[8])
    response = app.response_class(
        response = json.dumps(UnzippedFiles),
        status = 200,
        mimetype = 'application/json'
    )
    return response

if __name__ == "__main__":
    app.run(debug=True)