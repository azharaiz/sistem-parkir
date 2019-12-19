import RPi.GPIO as GPIO
import os
import time
from datetime import datetime
from pyfingerprint.pyfingerprint import PyFingerprint
import hashlib

def readFP():
    try:
        print('Waiting for finger...')

        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)

        ## Searchs template
        result = f.searchTemplate()
        positionNumber = result[0]

        accuracyScore = result[1]

        if ( positionNumber == -1 ):
            print('No match found!')
            return ""
        else:
            dataFP = open("/home/pi/dataFP.txt", 'r').read().split(",")
            for usr in dataFP:
                print(usr)
                id_usr = usr.split('-')[0]
                name = usr.split('-')[1]
                if int(id_usr) == positionNumber:
                    break
            log = open("/home/pi/log.txt", "a+")
            date = datetime.now().strftime("%d %b %Y %H:%M:%S")
            image_name = datetime.now().strftime("%d%b%Y%H:%M:%S") + "_" + name
            log.write(date + ", " + name + ", " + image_name + "\n")
            log.close()
            print('ID: ' + str(positionNumber) + " NAME: " + name)
            print('The accuracy score is: ' + str(accuracyScore))
            return image_name

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        return ""

#Blinking function
def blink(pin):
  GPIO.output(pin,GPIO.HIGH)

def blinkoff(pin):
  GPIO.output(pin,GPIO.LOW)

fingerprint_detected = False
while (not fingerprint_detected):
    try:
        f = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)

        if ( f.verifyPassword() == False ):
            raise ValueError('The given fingerprint sensor password is wrong!')
        else:
            fingerprint_detected = True

    except Exception as e:
        print('The fingerprint  sensor could not be initialized!')
        print('Exception message: ' + str(e))
        exit(1)

GPIO.setmode(GPIO.BOARD)

servoPIN = 11
irPIN = 26
redLED = 40
yellowLED = 38
greenLED = 37

# set up GPIO output channel
GPIO.setup(redLED, GPIO.OUT)
GPIO.setup(yellowLED, GPIO.OUT)
GPIO.setup(greenLED, GPIO.OUT)
GPIO.setup(irPIN, GPIO.IN)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(2.5) # Initialization

#Init
OBJECTDETECTED = "Detected"
OBJECTNOTDETECTED = "Not detected"

irStatus = OBJECTNOTDETECTED

p.ChangeDutyCycle(1)
blink(yellowLED)
blinkoff(redLED)
blinkoff(greenLED)

try:
    photo_taken = False
    while True:
        if (GPIO.input(irPIN) == False and irStatus == OBJECTNOTDETECTED) :
            print("Object Detected")
            image_name = readFP()
            if (image_name and (not photo_taken)):
                photo_taken = True
                irStatus = OBJECTDETECTED
                os.system("fswebcam " + image_name + ".jpg")
                p.ChangeDutyCycle(7.5)
                blinkoff(yellowLED)
                blinkoff(redLED)
                blink(greenLED)
            if (not image_name):
                blinkoff(yellowLED)
                blink(redLED)
                time.sleep(1)
                blinkoff(redLED)
                blink(yellowLED)

        if (GPIO.input(irPIN) == True and irStatus == OBJECTDETECTED ):
            print("Object Not Detected")
            photo_taken = False
            irStatus = OBJECTNOTDETECTED
            p.ChangeDutyCycle(1)
            blinkoff(greenLED)
            blinkoff(redLED)
            blink(yellowLED)

except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()