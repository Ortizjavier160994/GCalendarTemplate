from flask import Flask, render_template, redirect, url_for, request, send_from_directory
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker
from urllib.parse import quote
import os
import datetime

app = Flask(__name__, static_url_path='')


MYDIR = os.path.dirname(__file__)

app.config["css"] = os.path.join(MYDIR + "/templates/")
app.config["js"] = os.path.join(MYDIR + "/templates/")

Bootstrap(app)
datepicker(app)


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



@app.route("/bitly/",methods=('GET','POST'))
def home():
#	app.send_static_file('./templates/bootstrap-combined.min.css')
#	send_css('/templates/bootstrap-combined.min.css')
	if (request.method == "POST"):
		url = getEncoded(request.form)
		return redirect(url_for("create_bitly",url = url))
	return render_template("index.html")


@app.route("/bitly/create/",methods=('GET','POST'))
def create_bitly(url):
	if (request.method == "POST"):
		pass
	return render_template("create_bitly.html",url = url)


@app.route('/')
def welcome():
  return render_template('welcome.html')

@app.route('/oauth/')
def oauth():
  code = request.args.get('code')
  client_id = '162d2656c9c91a22da1002d103a9ce99b18cb1bc'
  client_secret = 'e7c021443fe87d6c1dc510d3113f35d29c7dd8c4'
  redirect_uri = 'calendar-template.herokuapp.com/bitly/'

  payload = {'client_id': client_id, 'client_secret': client_secret, 'redirect_uri': redirect_uri, 'code': code}
  r = requests.post("https://api-ssl.bitly.com/oauth/access_token", data=payload)

  data = {}
  pairs = r.text.split('&')
  for pair in pairs:
    k, v = pair.split('=')
    data[k] = v

  return render_template('oauth.html', login=data['login'], access_token=data['access_token'])


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory(app.config["css"], filename = path, as_attachment=False)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory(app.config["js"], filename = path, as_attachment=False)

if __name__ == "__main__":
    app.run(debug=True)