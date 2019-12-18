from flask import Flask, render_template, send_from_directory
from helper import get_file, get_img

app = Flask(__name__)
    
@app.route("/")
def log():
    return render_template("log.html", logs=get_file())

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)