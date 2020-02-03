 # file emulator.py
 # date Feb 3, 2020
 # 
 # Copyright (C) 2020 Signove Tecnologia Corporation.
 # All rights reserved.
 # Contact: Signove Tecnologia Corporation (contact@signove.com)
 # 
 # $LICENSE_TEXT:BEGIN$
 # MIT License
 # 
 # Permission is hereby granted, free of charge, to any person obtaining a copy
 # of this software and associated documentation files (the "Software"), to deal
 # in the Software without restriction, including without limitation the rights
 # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 # copies of the Software, and to permit persons to whom the Software is
 # furnished to do so, subject to the following conditions:
 # 
 # The above copyright notice and this permission notice shall be included in all
 # copies or substantial portions of the Software.
 # 
 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 # FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 # LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 # SOFTWARE.
 # $LICENSE_TEXT:END$
 # 

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
