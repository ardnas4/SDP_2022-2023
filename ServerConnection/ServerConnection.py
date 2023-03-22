import socket, threading
# import tflite_runtime.interpreter as tflite
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import *
import select
from PIL import Image
import io
from Cryptography.fernet import Fernet as fer
import numpy as np
# https://discuss.python.org/t/python-sockets-servers-and-multi-threading/22103
# https://realpython.com/python-sockets/#background
# https://docs.python.org/3/library/threading.html#thread-objects

key = fer.generate_key()







class ServerConnection:
    def __init__(self, key):
        __cryptKeyPath = ""
        __serverInfo = ("127.", "12345")    # Need actual values
        __ModelInfo=("ModelPAth", "modelFile")   # Path and file of model
        # __AIConverter = None
        # self.ModelConvert(__AIConverter)
        __AIModel = tf.keras.models.load_model(model_path=self.GetModelFile())
        __cryptS=fer(key)
        __buffSize = 10000
        __numQueueClients = 12
        __accuracyThreshold = .7
        __timeoutSeconds = 100
  
    # Main loop
    def Run(self):
        mainSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mainSock.bind(self.GetServerInfo())
        print("Waiting for a client to connect...")
        mainSock.listen(self.GetClientQueueSize())
        while True:
            conn, addr = mainSock.accept()
            conn.setblocking(0) # Allows select function to control blocking so timeout is possible
            t = threading.Thread(target=self.HandleConnection, args = (conn, addr)).start()

    # When connection happens pass the established connection and address of client in a thread
    def HandleConnection(self, conn, addr):
        print(f"Connection transferred to thread from {addr}")

        # Could add some timeout
        while True:
            sel = select.select([conn], [], [], self.GetTimeoutDelay())
            if sel[0]:
                receivedInfo = self.DecryptMessage(conn.recv(self.GetBufferSize()))
            else:
                break
            # # Receive the size of the image file
            # image_size = int(client_socket.recv(1024).decode())
            # Receive the image data
            image_data = receivedInfo[2:]
            # while len(image_data) < image_size:
            #     image_data += client_socket.recv(1024)

            # # Write the image data to a file
            # with open('received_image.jpg', 'wb') as f:
            #     f.write(image_data)
            resType = int(receivedInfo[:1])
            # # Send an acknowledgment to the client
            # client_socket.sendall(b'ACK')

            if resType == 0:
                break
            elif resType == 1:
                # Call normal analysis
                # Indexes: 0=corresponding image, 1=accuracy, 2=plant type
                imgStats = self.ProcessImage(image_data)

                # Invoke resend of image (accuracy too low)
                if imgStats[1] < self.GetAccThresh():
                    conn.sendall(self.EncryptMessage(b'01'+self.CommunicationEndCharacter()))
                # Sends type of plant and message type 2
                else:
                    imgToSend = imgStats[0]
                    predAcc = imgStats[1]
                    predPlant= imgStats[2]
                    conn.sendall(self.EncryptMessage(b'10'+predPlant+ predAcc+ imgToSend+self.CommunicationEndCharacter()))
        conn.sendall(self.EncryptMessage(b'00'+self.CommunicationEndCharacter()))
        conn.close()
        print(f"Connection terminated with client, {addr}")

    # May have to make it so tflite gets passed in as a reference and not value
    # def ModelConvert(self, tfliteModel):
    #     converter = tflite.TFLiteConverter.from_saved_model(self.GetSavedModelPath())
    #     tfliteModel = converter.convert()
    #     with open(self.GetTfliteFile(), 'wb') as f:
    #         f.write(tfliteModel)

    # Returns tuple with, Indexes: 0=corresponding image, 1=accuracy, 2=plant type
    def ProcessImage(self, img):
        # img = tf.keras.utils.load_img(
        #     sunflower_path, target_size=(img_height, img_width)
        # )
        # pilImg = Image.frombytes('RGBA', (128,128), img, 'raw')

        pilImg = Image.open(io.BytesIO(img))
        img_array = tf.keras.utils.img_to_array(pilImg)
        img_array = tf.expand_dims(img_array, 0) # Create a batch

        predictions = self.__AIModel.predict(img_array)
        score = tf.nn.softmax(predictions[0])

        return ("image if possible",np.max(score),predictions)

    def EncryptMessage(self, msg):
        return self.__cryptS.encrypt(msg)
    
    def DecryptMessage(self, msg):
        return self.__cryptS.decrypt(msg)
    
    def GetServerInfo(self):
        return self.__serverInfo

    def GetIP(self):
        return self.__serverInfo[0]

    def GetPort(self):
        return self.__serverInfo[1]

    def GetSavedModelPath(self):
        return self.__ModelInfo[0]
    
    def GetModelFile(self):
        return self.__ModelInfo[1]
    
    def GetBufferSize(self):
        return self.__buffSize

    def GetClientQueueSize(self):
        return self.__numQueueClients

    def GetKeyLocation(self):
        return self.__cryptKeyPath
    
    def GetAccThresh(self):
        return self.__accuracyThreshold
    
    def CommunicationEndCharacter(self):
        return "0/"
    
    def GetTimeoutDelay(self):
        return self.__timeoutSeconds