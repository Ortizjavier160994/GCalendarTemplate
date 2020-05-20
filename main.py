from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from urllib.parse import quote


app = Flask(__name__)

def getEncoded(title,detail):
	return "https://calendar.google.com/calendar/render?action=TEMPLATE&text=" +\
		quote(title, safe='') + "&details=" + quote(detail, safe='')


@app.route("/",methods=('GET','POST'))
def home():
	if (request.method == "POST"):
		print(request.form.get("start-date"))
		return getEncoded(request.form.get("title"),request.form.get("detail"))
	return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)