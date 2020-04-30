import socket
import pygame
import pickle
import time
pygame.init()
 
# Set the width and height of the screen [width, height]



# Count the joysticks the computer has
joystick_count = pygame.joystick.get_count()
if joystick_count == 0:
    # No joysticks!
    print("Error, I didn't find any joysticks.")
else:
    # Use joystick #0 and initialize it
    my_joystick = pygame.joystick.Joystick(0)
    my_joystick.init()


SERVER = "10.0.0.48"
PORT = 6699
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
client.sendall(bytes("This is from Client",'UTF-8'))
data =  client.recv(1024)
print(data.decode())
while True:
 
    pygame.event.get()
   
    if joystick_count != 0:
        
        arm = my_joystick.get_axis(2)
        wrist_up = my_joystick.get_button(0)
        wrist_down = my_joystick.get_button(3)
        leftY = my_joystick.get_axis(1)
        rightY = my_joystick.get_axis(3)
        claw_close = my_joystick.get_button(1)
        claw_open = my_joystick.get_button(2)

        print(rightY)

        if claw_close == True:
            claw = 1
        elif claw_open == True:
            claw = -1
        else:
            claw = 0
            

        if leftY < 0.1 and leftY > -0.1:
            leftY = 0.0
        if rightY < 0.1 and rightY > -0.1:
            rightY = 0.0
        if arm < 0.1 and arm > -0.1:
                arm = 0.0

        if wrist_up == True:
            wrist = .2
        elif wrist_down == True:
            wrist = -.2
        else:
            wrist = 0.0

        leftY = round(leftY, 2)
        rightY = round(rightY, 2)
        arm = round(arm, 2)
        d = {0:leftY, 1: rightY, 2:arm, 3: wrist, 4: claw}
        msg = pickle.dumps(d)

        client.sendall(msg)
        time.sleep(0.2)
       
pygame.quit