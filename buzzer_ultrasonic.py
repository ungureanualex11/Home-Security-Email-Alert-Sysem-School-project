

#import the libraries used
import time
import smtplib
import pigpio
import RPi.GPIO as GPIO

#create an instance of the pigpio library
pi = pigpio.pi()

#define the pin used by the Buzzer
#this pin will be used by the pigpio library
#which takes the pins in GPIO forms
#we will use GPIO18, which is pin 12
buzzer = 18

#set the pin used by the buzzer as OUTPUT
pi.set_mode(buzzer, pigpio.OUTPUT)

GPIO.setmode(GPIO.BOARD)

#define the pins used by the ultrasonic module
trig = 32
echo = 38

#set the trigger pin as OUTPUT and the echo as INPUT
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)


server=smtplib.SMTP('smtp.gmail.com',587)
sended=0
server.starttls()
server.login("email@gmail.com","parola")
msg="Cineva este la usa ! "

def calculate_distance():
    #set the trigger to HIGH
    GPIO.output(trig, GPIO.HIGH)

    #sleep 0.00001 s and the set the trigger to LOW
    time.sleep(0.00001)
    GPIO.output(trig, GPIO.LOW)

    #save the start and stop times
    start = time.time()
    stop = time.time()

    #modify the start time to be the last time until
    #the echo becomes HIGH
    while GPIO.input(echo) == 0:
        start = time.time()

    #modify the stop time to be the last time until
    #the echo becomes LOW
    while  GPIO.input(echo) == 1:
        stop = time.time()

    #get the duration of the echo pin as HIGH
    duration = stop - start

    #calculate the distance
    distance = 34300/2 * duration

    if distance < 0.5 and distance > 400:
        return 0
    else:
        #return the distance
        return distance

try:
    while True:
        if calculate_distance() < 25:
            #turn on the buzzer at a frequency of
             #500Hz for 50 ms
            pi.hardware_PWM(buzzer, 500, 500000)
            time.sleep(0.05)
        
            #turn off the buzzer and wait 50 ms
            pi.hardware_PWM(buzzer, 0, 0)
            time.sleep(0.05)
                
            if sended == 0:
               server.sendmail("emailplacuta@gmail.com","destinatar@gmail.com",msg)
               sended = 1;
                      

        else:
            if sended == 1:
                server.sendmail("emailplacuta@gmail.com","destinatar@gmail.com","Vizitatorul a plecat")
            #turn off the buzzer
            pi.hardware_PWM(buzzer, 0, 0)
            sended = 0;

        #wait 100 ms before the next run
        time.sleep(0.1)

except KeyboardInterrupt:
    pass
server.quit()
#turn off the buzzer
pi.write(buzzer, 0)
#stop the connection with the daemon
pi.stop()

#clean all the used ports
GPIO.cleanup()
