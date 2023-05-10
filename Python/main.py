from flask import Flask, render_template, request, redirect, url_for
import time

app = Flask(__name__, static_folder=r'C:\Users\tim\PycharmProjects\MensaApp\static')

academica_main = {}
academica_secret = {}
academica_first = {}
academica_bp = {}
academica_wok = {}
vita = {}
time_limit = 1800


@app.route('/', methods=['POST', 'GET'])
def start_page():
    delete_old(academica_main)
    customers = {"am": len(academica_main),
                 "as": len(academica_secret),
                 "af": len(academica_first),
                 "abp": len(academica_bp),
                 "aw": len(academica_wok),
                 "vita": len(vita)}
    return render_template("index.html", customers=customers)


@app.route("/academica_main", methods=['POST', 'GET'])
def academica_main_f():
    name = request.form.get("name")
    x = request.form.get("x")
    y = request.form.get("y")
    submit_time = time.time()
    if name is not None:
        delete_old(academica_main)
        academica_main[name] = [x, y, submit_time]
        print(academica_main)
    return render_template("academica_main.html", locations=academica_main)


@app.route("/academica_secret", methods=['POST', 'GET'])
def academica_secret_f():
    return render_template("baustelle.html", locations=academica_secret)


@app.route("/academica_first", methods=['POST', 'GET'])
def academica_first_f():
    return render_template("baustelle.html", locations=academica_first)


@app.route("/academica_wok", methods=['POST', 'GET'])
def academica_wok_f():
    return render_template("baustelle.html", locations=academica_wok)


@app.route("/academica_bp", methods=['POST', 'GET'])
def academica_bp_f():
    return render_template("baustelle.html", locations=academica_bp)


@app.route("/vita", methods=['POST', 'GET'])
def vita_f():
    return render_template("baustelle.html", locations=vita)


def delete_old(locations):
    current_time = time.time()
    valid_locations = {}
    for key, value in locations.items():
        if value is not None:
            if current_time - value[2] < time_limit:
                valid_locations[key] = value

    locations.clear()
    locations.update(valid_locations)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
