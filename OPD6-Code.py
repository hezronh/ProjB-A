import RPi.GPIO as GPIO
import time
GPIO.setmode( GPIO.BCM )
GPIO.setwarnings( 0 )

print( "sr04 print" )

sr04_trig = 20
sr04_echo = 21

GPIO.setup( sr04_trig, GPIO.OUT )
GPIO.setup( sr04_echo, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )

def sr04( trig_pin, echo_pin ):
   """
   Return the distance in cm as measured by an SR04
   that is connected to the trig_pin and the echo_pin.
   These pins must have been configured as output and input.s
   """
   GPIO.output(trig_pin, True)
   time.sleep(0.1)
   GPIO.output(trig_pin, False)

   startTijd = 0
   stopTijd = 0

   while GPIO.input(echo_pin) == 0:
      startTijd = time.time()

   while GPIO.input(echo_pin) == 1:
      stopTijd = time.time()

   tijdsVerschil = stopTijd - startTijd
   afstand = (tijdsVerschil * 34300) / 2

   return afstand


while True:
   print( sr04( sr04_trig, sr04_echo ))
   time.sleep( 0.5 )
