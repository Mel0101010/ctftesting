from flask import Flask, request

app = Flask(__name__)

FLAG = "fakeflag"

@app.route("/")
def home():
    return "Welcome"

@app.route("/debug")
def debug():
    if request.args.get("admin") == "1":
        return FLAG
    return "Forbidden"

app.run(host="0.0.0.0", port=5000)
