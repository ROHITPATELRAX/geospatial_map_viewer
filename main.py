import io
import os
import json
from flask import Flask,Response,redirect,request,render_template,url_for
from dotenv import load_dotenv

#Flask Form imports
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,validators,ValidationError
from wtforms.validators import DataRequired,Email

from zipfile import ZipFile
import geopandas as gpd
import matplotlib.pyplot as plt
from werkzeug.utils import secure_filename


load_dotenv()
env = os.environ

BASE_DIR =  os.path.dirname(os.getcwd())

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def home():
    return redirect("/uploads","file")

@app.route("/uploads",methods=["GET","POST"])
def uploader():
    if request.method == "POST":
        filename = None
        try:
            if 'file' in request.files:
                file = request.files['file']
                if str(file.filename).split(".")[-1]=="zip":
                    with ZipFile(io.BytesIO(file.read()), 'r') as zip:
                        foldername = str(file.filename).replace(".zip","")
                        foldernamewithpath = BASE_DIR+'/geospatial_map_view/tmp/' +str(file.filename).replace(".zip","")
                        zip.extractall(foldernamewithpath)

                        imagelist = list()

                        imageProvider(foldername,foldernamewithpath,imagelist)

                        print(imagelist)

                        if len(imagelist)>0:
                            message = "File successfully uploaded"
                        else:
                            message = ".shp file not found"
                else:
                    message = "Invalid file format"

        except Exception as msg:
            print(msg)
            message = msg
        return render_template('uploader.html',mainDict = {'message':message,'filename':imagelist})

    else:
        return render_template('uploader.html',mainDict = {'message':None})
    
def imageProvider(foldername,foldernamewithpath,imagelist):
    for file in os.listdir(foldernamewithpath):
        print(file)
        if os.path.isdir(foldernamewithpath+'/'+file):
            imageProvider(file,foldernamewithpath+'/'+file,imagelist)
        else:
            if file.endswith(".shp"):
                df = gpd.read_file(foldernamewithpath+"/"+file)
                ax = df.plot()
                imagePath1 = foldername + ".png"
                imagePath = BASE_DIR+"/geospatial_map_view/static/media/"+imagePath1
                plt.savefig(imagePath, dpi=300, bbox_inches='tight')
                imagelist.append({"image":imagePath1,"columns":df.columns.to_list()})

@app.route("/imageViewer",methods=["POST"])
def imageReader():
    item_list = request.form.getlist('item[]')
    item_list123 = [eval(item) for item in item_list]
    print(item_list123)
    for i in range(0,len(item_list123)):
        if "media/" not in item_list123[i]['image']:
            item_list123[i]['image'] = "media/"+item_list123[i]['image']
    return render_template("imageviewer.html",imagePath=item_list123)

if __name__=="__main__":
    app.run(debug=True)