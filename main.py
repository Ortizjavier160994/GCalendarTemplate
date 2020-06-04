from flask import Flask, render_template, redirect, url_for, request, send_from_directory, flash
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker
from urllib.parse import quote
import os
import datetime
import requests


app = Flask(__name__, static_url_path='')
app.secret_key = 'asrtarstaursdlarsn'


MYDIR = os.path.dirname(__file__)

app.config["css"] = os.path.join(MYDIR + "/templates/")
app.config["js"] = os.path.join(MYDIR + "/templates/")

Bootstrap(app)
datepicker(app)

url = ""
api_key = ""

def formatDate(date):
	date_time = date.split(" ")
	d = date_time[0].split("/")
	t = date_time[1].split(":")
	return d[2] + d[1] + d[0] + "T" + t[0] + t[1] + t[2] + "Z"

def getEncoded(form):
	dt_start = formatDate(form.get("start"))
	dt_end = formatDate(form.get("end"))
	return "https://calendar.google.com/calendar/render?action=TEMPLATE&text=" +\
		quote(form.get("title"), safe='') + "&details=" + quote(form.get("detail"), safe='') + "&dates=" + dt_start + "/" + dt_end + "&sf=true" + "&location=" + quote(form.get("location"),safe='')



@app.route("/create-template/",methods=('GET','POST'))
def home():
	global url
#	app.send_static_file('./templates/bootstrap-combined.min.css')
#	send_css('/templates/bootstrap-combined.min.css')
	if (request.method == "POST"):
		url = getEncoded(request.form)
		return redirect("/create-template/bitly/")
	return render_template("index.html")


	"""
		{
		"domain": "bit.ly",
		"title": "string",
		"group_guid": "string",
		"tags": [
		"string"
		],
		"deeplinks": [
		{}
		],
		"long_url": "string"
		}
	"""
@app.route("/create-template/bitly/",methods=('GET','POST'))
def create_bitly():
	global url
	global api_key
	print(url)
	if (request.method == "POST"):
		print("POST bitly")
		print("API",api_key)
		print(request.form.get("new_url"))
		print(request.form.get("new_url_title"))
		payload = {'domain': quote("bit.ly/"+request.form.get("new_url"), safe =""), 'title': quote(request.form.get("new_url_title"), safe= ''), 'long_url': url}
		headers = {'Authorization' : "Bearer " + api_key, "Content-Type": 'application/json'}
		r = requests.post("https://api-ssl.bitly.com/bitlinks", json=payload, headers = headers)
		print(r.content)
		if(r.status_code == 200):
			flash("Bien ahí perraca", "Success")
		else:
			flash("Recalculando", "Danger")
		return redirect("/create-template/")
	return render_template("create_bitly.html",url = url)


@app.route('/')
def welcome():
  return render_template('welcome.html')

@app.route('/bitly/')
def oauth():
	global api_key
	code = request.args.get('code')
	print("Codigo: ", code)
	client_id = '162d2656c9c91a22da1002d103a9ce99b18cb1bc'
	client_secret = '759c3cbc5fd77a6ddde76ea57faa266797228472'
	redirect_uri = 'https://calendar-template.herokuapp.com/bitly/'

	payload = {'client_id': client_id, 'client_secret': client_secret, 'redirect_uri': redirect_uri, 'code': code}
	r = requests.post("https://api-ssl.bitly.com/oauth/access_token", data=payload)	

	data = {}
	pairs = r.text.split('&')
	for pair in pairs:
		try:
			k, v = pair.split('=')
			data[k] = v
		except:
	  		continue

	api_key = data["access_token"]

	return redirect("/create-template/")


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory(app.config["css"], filename = path, as_attachment=False)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory(app.config["js"], filename = path, as_attachment=False)

if __name__ == "__main__":
    app.run(debug=True)