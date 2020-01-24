from ecg import ECG
from flask import Flask, request, render_template, redirect, url_for
import netifaces as ni

app=Flask(__name__)
ecgcontrol = ECG()

@app.route("/")
def index():
   return render_template('index.html', nsrbpm=str(ecgcontrol.getBPM()), squareperiod=str(ecgcontrol.getSquarePeriod()))

@app.route("/ecg/bpm", methods=["POST"])
def ecg_nsr():
    bpm=request.form["nsrbpm"]
    ecgcontrol.setNSR(int(bpm))
    toredirect = request.form["redirect"]
    if(toredirect == "false"):
        return "";
    return redirect(url_for("index"))

@app.route("/ecg/arrithymia", methods=["POST"])
def ecg_arrithymia():
    arrythmiaId = request.form["arrythmiaId"]
    ecgcontrol.setArrithymia(int(arrythmiaId))
    return redirect(url_for("index"))

@app.route("/ecg/square", methods=["POST"])
def ecg_square():
    squareperiod=request.form["squareperiod"]
    highValue=request.form["highValue"]
    lowValue=request.form["lowValue"]
    ecgcontrol.setSquare(int(squareperiod), highValue, lowValue)
    return redirect(url_for("index"))

@app.route("/ecg/status")
def getstatus():
    return str(ecgcontrol.getStatus())

if __name__=="__main__":
    ecgcontrol.start()
    app.run(host='0.0.0.0')
