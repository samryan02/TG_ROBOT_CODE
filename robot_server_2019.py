import socket
import pickle
from adafruit_servokit import ServoKit
LOCALHOST = "0.0.0.0"
PORT = 6699
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((LOCALHOST, PORT))
server.listen(1)
kit = ServoKit(channels=16, address=96)

print("Server started")
print("Waiting for client request..")
while True:

    clientConnection,clientAddress = server.accept()
    print("Connected clinet :" , clientAddress)
    data = clientConnection.recv(1024)
    print("From Client :" , data.decode())
    clientConnection.send(bytes("Successfully Connected to Server!!",'UTF-8'))
    while True:
        try:
            data = clientConnection.recv(1024)
        except:
            kit.continuous_servo[2].throttle =  -0.1
            kit.continuous_servo[3].throttle =  -0.1
            kit.continuous_servo[4].throttle =  -0.1
            kit.continuous_servo[0].throttle =  -0.1
            kit.continuous_servo[1].throttle =  -0.1
            exit()
        recd = pickle.loads(data)

        left_drive = -0.1
        right_drive = -0.1
        arm = -0.1
        wrist = -0.1
        claw = -0.1
        print("leftY: " , recd[0])
        print("rightY: " , recd[1])
        left_drive = recd[0]
        right_drive = recd[1]
        arm = recd[2]
        wrist = recd[3]
        claw = recd[4]
        #print("From Client :" , recd)
        left_drive = left_drive - 0.1
        right_drive = right_drive - 0.1
        arm = arm - 0.1	
        wrist = wrist - 0.1
        claw = claw - 0.1
        if claw < -1.0:
                claw = -1.0
        if left_drive < -1.0:
                left_drive = -1.0
        if right_drive < -1.0:
                right_drive = -1.0
        if arm < -1.0:
                arm = -1.0
        if wrist < -1.0:
                wrist = -1.0
        kit.continuous_servo[2].throttle =  arm
        kit.continuous_servo[3].throttle =  wrist
        kit.continuous_servo[4].throttle =  claw
        kit.continuous_servo[0].throttle =  left_drive 
        kit.continuous_servo[1].throttle =  right_drive