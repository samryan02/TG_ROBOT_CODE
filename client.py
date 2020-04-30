import socket
import struct
import pickle
import base64
import numpy as np
import cv2

def rescale_frame(old_image, percent):
    width = int(old_image.shape[1] * percent/ 100)
    height = int(old_image.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(old_image, dim, interpolation=cv2.INTER_AREA)

CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CLIENT_SOCKET.connect(('192.168.1.223', 8485))
CONNECTION = CLIENT_SOCKET.makefile('wb')
print("this is client")

DATA = b""
PAYLOAD_SIZE = struct.calcsize(">L")
print("PAYLOAD_SIZE: {}".format(PAYLOAD_SIZE))

while True:
    while len(DATA) < PAYLOAD_SIZE:
        print("Recv: {}".format(len(DATA)))
        DATA += CLIENT_SOCKET.recv(4096)

    print("Done Recv: {}".format(len(DATA)))
    PACKAGED_MSG_SIZE = DATA[:PAYLOAD_SIZE]
    DATA = DATA[PAYLOAD_SIZE:]
    MSG_SIZE = struct.unpack(">L", PACKAGED_MSG_SIZE)[0]
    print("MSG_SIZE: {}".format(MSG_SIZE))
    while len(DATA) < MSG_SIZE:
        DATA += CLIENT_SOCKET.recv(4096)
    FRAME_DATA = DATA[:MSG_SIZE]
    DATA = DATA[MSG_SIZE:]

    IMAGE_DATA = pickle.loads(FRAME_DATA, fix_imports=True, encoding="bytes")
    RAW_IMAGE = base64.b64decode(IMAGE_DATA)
    IMAGE = np.frombuffer(RAW_IMAGE, dtype=np.uint8)
    FRAME = cv2.imdecode(IMAGE, 1)
    FRAME = rescale_frame(FRAME, percent=300)
    cv2.imshow('ImageWindow', FRAME)
    cv2.waitKey(1)
