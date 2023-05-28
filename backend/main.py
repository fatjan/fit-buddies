from flask import Flask

app = Flask(__name__)

@app.route("/")
def hellow_word():
    return f"Hello World!"