from machine import Pin, PWM
from time import sleep

DUTY = 22000	# Ranges from 0 to 65025

M1A = PWM(Pin(2))
M1B = PWM(Pin(3))
M2A = PWM(Pin(4))
M2B = PWM(Pin(5))
M3A = PWM(Pin(6))
M3B = PWM(Pin(7))
M4A = PWM(Pin(8))
M4B = PWM(Pin(9))

M1A.freq(1000)
M1B.freq(1000)
M2A.freq(1000)
M2B.freq(1000)
M3A.freq(1000)
M3B.freq(1000)
M4A.freq(1000)
M4B.freq(1000)

def stop():
    M1A.duty_u16(0)
    M2A.duty_u16(0)
    M3A.duty_u16(0)
    M4A.duty_u16(0)
    M1B.duty_u16(0)
    M2B.duty_u16(0)
    M3B.duty_u16(0)
    M4B.duty_u16(0)
    
def forward():
    M1A.duty_u16(DUTY)
    M2A.duty_u16(DUTY)
    M3A.duty_u16(DUTY)
    M4A.duty_u16(DUTY)

def backward():
    M1B.duty_u16(DUTY)
    M2B.duty_u16(DUTY)
    M3B.duty_u16(DUTY)
    M4B.duty_u16(DUTY)

def left():
    M1B.duty_u16(DUTY)
    M2A.duty_u16(DUTY)
    M3B.duty_u16(DUTY)
    M4A.duty_u16(DUTY)

def right():
    M1A.duty_u16(DUTY)
    M2B.duty_u16(DUTY)
    M3A.duty_u16(DUTY)
    M4B.duty_u16(DUTY)

def crableft():
    M1B.duty_u16(DUTY)
    M2A.duty_u16(DUTY)
    M3A.duty_u16(DUTY)
    M4B.duty_u16(DUTY)

def crabright():
    M1A.duty_u16(DUTY)
    M2B.duty_u16(DUTY)
    M3B.duty_u16(DUTY)
    M4A.duty_u16(DUTY)

if __name__ == "__main__":
    forward()
    sleep(1)
    stop()
    backward()
    sleep(1)
    stop()
    left()
    sleep(1)
    stop()
    right()
    sleep(1)
    stop()
    crableft()
    sleep(1)
    stop()
    crabright()
    sleep(1)
    stop()
    
