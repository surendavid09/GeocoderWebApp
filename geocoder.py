from flask import Flask, render_template, request, send_file
import pandas
import os
from geopy.geocoders import ArcGIS
from werkzeug.utils import secure_filename
import datetime

app = Flask(__name__)
nom=ArcGIS()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods=['POST'])
def success():
    global filename
    if request.method=="POST":
        file=request.files["file"]
        try:
            data = pandas.read_csv(file)
            x=nom.geocode(data["Address"][0])
        except:
            return render_template("index.html", text="Input was not a CSV File or did not have an Address column")

        data["Coordinates"]=data["Address"].apply(nom.geocode)
        data["Latitude"]=data["Coordinates"].apply(lambda x: x.latitude if x != None else None)
        data["Longitude"]=data["Coordinates"].apply(lambda x: x.longitude if x != None else None)
        del data["Coordinates"]
        filename=datetime.datetime.now().strftime("%Y-%m-%d -%H-%M-%S-%f"+".csv")
        data.to_csv(filename, index=True)
        result = data.to_html()

        return render_template("index.html", text=data.to_html(), btn="download.html")


@app.route("/download")
def download():
    return send_file(filename, attachment_filename="modified.csv", as_attachment=True)

if __name__ == "__main__":
    app.debug=True
    app.run()
