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
	return d[2] + d[1] + d[0] + "T" + str(int(t[0])+3) + t[1] + t[2] + "Z"

def getEncoded(form):
	dt_start = formatDate(form.get("start"))
	dt_end = formatDate(form.get("end"))
	return "https://calendar.google.com/calendar/render?action=TEMPLATE&text=" +\
		quote(form.get("title"), safe='') + "&details=" + quote(form.get("detail"), safe='') + "&dates=" + dt_start + "/" + dt_end + "&sf=true" + "&location=" + quote(form.get("location"),safe='')




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
	global api_key
	if (request.method == "POST"):
		#+request.form.get("new_url")
		global url
		print(url)
		payload = {'domain': "bit.ly", 'title': request.form.get("new_url_title"), 'long_url': url}
		headers = {'Authorization' : f"{api_key}"}
		r = requests.post("https://api-ssl.bitly.com/v4/bitlinks", json=payload, headers = headers)
		print("Url to post",r.request.url)
		print("Headers:",r.request.headers)
		print("Data sent:",r.request.body)
		print("Response content:",r.content)
		if(r.status_code >= 200 and r.status_code < 300):
			flash("Bien ahí perraca", "Success")
		else:
			flash("Recalculando", "Danger")
		return redirect("/create-template/")
	else:
		return render_template("create_bitly.html",url = url)



#create-template/
@app.route("/",methods=('GET','POST'))
def home():
#	app.send_static_file('./templates/bootstrap-combined.min.css')
#	send_css('/templates/bootstrap-combined.min.css')
	if (request.method == "POST"):
		return redirect(getEncoded(request.form))
	return render_template("index.html")


#ex-home
@app.route('/notfound')
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