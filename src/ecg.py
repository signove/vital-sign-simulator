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
