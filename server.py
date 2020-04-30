import cv2
import socket
import struct
import pickle
import base64

print("this is server")

HOST=''
PORT=8485

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST,PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

conn,addr=s.accept()


cam = cv2.VideoCapture(0)

img_counter = 0
print("this is server")
#encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:
    ret, frame = cam.read()
    #result, frame = cv2.imencode('.jpg', frame, encode_param)
    frame = cv2.resize(frame, (640, 480))
    encoded, buf = cv2.imencode('.jpg', frame)
    image = base64.b64encode(buf)
    data = pickle.dumps(image, 0)
    size = len(data)


    print("{}: {}".format(img_counter, size))
    conn.sendall(struct.pack(">L", size) + data)
    img_counter += 1

cam.release()