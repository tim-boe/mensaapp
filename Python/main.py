from flask import Flask, render_template, request, redirect, url_for
import csv
import time

app = Flask(__name__, static_folder=r'C:\Users\tim\PycharmProjects\MensaApp\static')

fc_path = r"C:\Users\tim\Documents\mensaapp\data\violations.csv"

academica_main = {}
academica_secret = {}
academica_first = {}
academica_bp = {}
academica_wok = {}
vita = {}
rw_festival = {}
rw_camping = {}
time_limit = 1800


@app.route('/', methods=['POST', 'GET'])
def start_page():
    delete_old(academica_main)
    customers = {"am": len(academica_main),
                 "as": len(academica_secret),
                 "af": len(academica_first),
                 "abp": len(academica_bp),
                 "aw": len(academica_wok),
                 "vita": len(vita),
                 "rwf": len(rw_festival),
                 "rwc": len(rw_camping)}

    return render_template("index.html", customers=customers)


@app.route("/academica_main", methods=['POST', 'GET'])
def academica_main_f():
    name = request.form.get("name")
    x = request.form.get("x")
    y = request.form.get("y")
    submit_time = time.time()
    if name is not None:
        if len(name) > 50:
            return "ne, dann eben ohne dich...."
        delete_old(academica_main)
        academica_main[name] = [x, y, submit_time]
        print(academica_main)
    return render_template("academica_main.html", locations=academica_main)


@app.route("/rw_festival", methods=['POST', 'GET'])
def rw_festival_f():
    name = request.form.get("name")
    x = request.form.get("x")
    y = request.form.get("y")
    submit_time = time.time()
    if name is not None:
        delete_old(rw_festival, limit=3600)
        rw_festival[name] = [x, y, submit_time]
        print(rw_festival)
    return render_template("rw_festival.html", locations=rw_festival)


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


@app.route("/fuckcars", methods=['POST', 'GET'])
def fuckcars_f():
    if request.method == "POST":
        timestamp = request.form.get("time")
        overtake_counts = request.form.get("overtakes")
        distance = request.form.get("distance")
        other_violations = request.form.get("other")
        csv_string = str(timestamp) + ";" + str(overtake_counts) + ";" + str(distance) + ";" + str(other_violations)
        with open(fc_path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([csv_string])
        return "tank you"
    return render_template("fuckcars.html")


def delete_old(locations, limit=time_limit):
    current_time = time.time()
    valid_locations = {}
    for key, value in locations.items():
        if value is not None:
            if current_time - value[2] < limit:
                valid_locations[key] = value

    locations.clear()
    locations.update(valid_locations)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
