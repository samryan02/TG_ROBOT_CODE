from __future__ import division
import time
import pygame
# Import the PCA9685 module.
import Adafruit_PCA9685
import cv2
pygame.init()
cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

pwm = Adafruit_PCA9685.PCA9685()
motor_1 = 0
motor_2 = 0
x_coord = 0

def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 50       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

pwm.set_pwm_freq(50)

print('Moving servo on channel 0, press Ctrl-C to quit...')

joystick_count = pygame.joystick.get_count()
if joystick_count == 0:
     print("Error, I didn't find any joysticks.")
else:
    my_joystick = pygame.joystick.Joystick(0)
    my_joystick.init()
if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while True:
       
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if joystick_count != 0:
            vert_axis_pos2 = my_joystick.get_axis(1)
            vert_axis_pos = my_joystick.get_axis(4)
            Z_axis_pos = my_joystick.get_axis(2)
            Z_axis_pos2 = my_joystick.get_axis(5)
            top_motor = (185 + Z_axis_pos * 309) + Z_axis_pos2 * 185 + 124
        
        motor_1 = (185  * vert_axis_pos + 309)
        motor_2 = (185  * vert_axis_pos2 + 309) 
        pwm.set_pwm(0, 0, int(motor_1))
        pwm.set_pwm(11, 0, int(motor_2))
        pwm.set_pwm(12, 0, int(top_motor))
        pwm.set_pwm(15, 0, int(top_motor))
    
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
pygame.quit()
cv2.destroyWindow("preview")
vc.release()