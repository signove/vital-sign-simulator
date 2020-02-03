 # file gpiocontrol.py
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
import RPi.GPIO as gpio


lowPins = [13, 19, 26]
highPins = [6]

run = True

gpio.setmode(gpio.BCM)# se for usar a referencia para GPIO da rpi 2 e 3
#gpio.setmode(gpio.BOARD)# se for usar a referencia para a posicao na placa da rpi 2 e 3

while run:
    for i in (lowPins + highPins):
        print "setup " + str(i)
        gpio.setup(i, gpio.OUT)

    for i in highPins:
        print "HIGH " + str(i)
        gpio.output(i, gpio.HIGH)

    for i in lowPins:
        print "LOW " + str(i)
        gpio.output(i, gpio.LOW)

    res = raw_input("Sair (S/n)? ")

    if res == "S":
        run = False