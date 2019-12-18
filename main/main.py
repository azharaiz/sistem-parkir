import RPi.GPIO as GPIO
def turn_on(led):
    GPIO.output(led, GPIO.HIGH)

def turn_off(led):
    GPIO.output(led, GPIO.LOW)

def clean():
    GPIO.cleanup()

LED_YELLOW = 12
LED_RED = 10
LED_GREEN = 13
SERVO = 20
FINGERPRINT = 21
