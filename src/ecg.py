 # file ecg.py
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

from ctypes import cdll
import ctypes
import json
lib = cdll.LoadLibrary('./libecg.so')

class ECG(object):
    def __init__(self):
        self.obj = lib.ecg_new()
        self.squarePeriod = 500
        self.squareHighValue = 550
        self.squareLowValue = 50

    def start(self):
        lib.ecg_start(self.obj)

    def setNSR(self, bpm):
        lib.ecg_setNSR(self.obj, bpm)

    def setCurve(self, curve):
        lib.ecg_setCurve(self.obj, curve)

    def getBPM(self):
        return lib.ecg_getBPM(self.obj)

    def setArrithymia(self, arrythmiaId):
        lib.ecg_setArrhythmia(self.obj, arrythmiaId)

    def setSquare(self, period, highValue=500, lowValue=0):
        self.squarePeriod = period
        self.squareHighValue = int(highValue)
        self.squareLowValue = int(lowValue)
        if self.squareHighValue > 4095:
            self.squareHighValue = 4095
        if self.squareHighValue < 0:
            self.squareHighValue = 0
        if self.squareLowValue > 4095:
            self.squareLowValue = 4095
        if self.squareLowValue < 0:
            self.squareLowValue = 0
        lib.ecg_setSquare(self.obj, int(self.squarePeriod), self.squareHighValue, self.squareLowValue)

    def getStatus(self):
        mode = lib.ecg_getMode(self.obj)
        ret = { "mode":mode, "squareLowValue":self.squareLowValue, "squareHighValue":self.squareHighValue, "squarePeriod":self.squarePeriod}
        return json.dumps(ret, ensure_ascii=False)

    def getSquarePeriod(self):
        return lib.ecg_getSquarePeriod(self.obj)
