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