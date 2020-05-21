from flask import Flask, render_template, redirect, url_for, request, send_from_directory
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker
from urllib.parse import quote
import os


app = Flask(__name__, static_url_path='')


MYDIR = os.path.dirname(__file__)

app.config["css"] = os.path.join(MYDIR + "/templates/")
app.config["js"] = os.path.join(MYDIR + "/templates/")

Bootstrap(app)
datepicker(app)


def getEncoded(title,detail):
	return "https://calendar.google.com/calendar/render?action=TEMPLATE&text=" +\
		quote(title, safe='') + "&details=" + quote(detail, safe='')




@app.route("/",methods=('GET','POST'))
def home():
#	app.send_static_file('./templates/bootstrap-combined.min.css')
#	send_css('/templates/bootstrap-combined.min.css')
	if (request.method == "POST"):
		print("submitted")
		print(request.form.get("start"))
		print(request.form.get("end"))
		return redirect(getEncoded(request.form.get("title"),request.form.get("detail")))
	return render_template("index.html")


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory(app.config["css"], filename = path, as_attachment=False)

@app.route('/js/<path:path>')
def send_js(path):
    return ssend_from_directory(app.config["js"], filename = path, as_attachment=False)

if __name__ == "__main__":
    app.run(debug=True)