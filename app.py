from flask import Flask, render_template, request, redirect, url_for
import os
from messenger import MessengerService

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

service = MessengerService()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        cookies = request.form.get("cookies")
        uid = request.form.get("uid")
        speed = int(request.form.get("speed", 10))
        haters = request.form.get("haters")

        file = request.files["messages"]
        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(path)

        with open(path, "r", encoding="utf-8") as f:
            messages = [l.strip() for l in f if l.strip()]

        service.start(
            cookies=cookies,
            uid=uid,
            messages=messages,
            speed=speed,
            haters_name=haters
        )

        return redirect(url_for("status"))

    return render_template("index.html")


@app.route("/status")
def status():
    return f"Running: {service.running}"


@app.route("/stop")
def stop():
    service.stop()
    return "Stopped"


if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
