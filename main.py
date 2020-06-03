from flask import Flask, render_template, redirect, url_for, request, send_from_directory
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker
from flask_oautlib.provider import OAuth2Provider
from urllib.parse import quote
import os
import datetime

app = Flask(__name__, static_url_path='')


MYDIR = os.path.dirname(__file__)

app.config["css"] = os.path.join(MYDIR + "/templates/")
app.config["js"] = os.path.join(MYDIR + "/templates/")

Bootstrap(app)
datepicker(app)
oauth = OAuth2Provider(app)


def formatDate(date):
	date_time = date.split(" ")
	d = date_time[0].split("/")
	t = date_time[1].split(":")
	return d[2] + d[1] + d[0] + "T" + t[0] + t[1] + t[2] + "Z"

def getEncoded(form):
	dt_start = formatDate(form.get("start"))
	dt_end = formatDate(form.get("end"))
	return "https://calendar.google.com/calendar/render?action=TEMPLATE&text=" +\
		quote(form.get("title"), safe='') + "&details=" + quote(form.get("detail"), safe='') + "&dates=" + dt_start + "/" + dt_end + "&sf=true" + "&location=" + form.get("location")



@app.route("/",methods=('GET','POST'))
def home():
#	app.send_static_file('./templates/bootstrap-combined.min.css')
#	send_css('/templates/bootstrap-combined.min.css')
	if (request.method == "POST"):
		return redirect(getEncoded(request.form))
	return render_template("index.html")


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory(app.config["css"], filename = path, as_attachment=False)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory(app.config["js"], filename = path, as_attachment=False)

if __name__ == "__main__":
    app.run(debug=True)