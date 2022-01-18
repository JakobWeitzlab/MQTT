import tkinter as tk
from tkinter import ttk
from queue import Queue
import time
import random

#========external librarys========
import paho.mqtt.client as mqtt

#========definitions========#
broker_address="172.104.234.24" #Linode Broker
port = 1883
topicHouseMainLight = "house/Light/main-light"
topicTemperaturSensor = "house/temperature/sensor1"
benutzer = "lukas"
passwort = "lukas"
connectionStatus = "not connected"
_running = True

#========Queue========#
q = Queue()


class Client():
    def __init__(self):
        self.client = mqtt.Client()
        self.client.username_pw_set(username = benutzer, password=passwort)
        self.client.on_connect = self.on_connect
        self.client.connect(broker_address, port)
        self.client.subscribe(topicTemperaturSensor)
        self.client.loop_start()

    def on_message(self, client, userdata, msg):      
        q.put(str(msg.payload))
        #print("\n" + topicTemperaturSensor + " " + str(msg.payload))        
                
    def ReceiveMessage(self):
        self.client.on_message = self.on_message
        
    def PublishMessage(self, topic, msgData):
        self.client.publish(topic = topic, payload = msgData)

    def on_connect(self, client, userdata, flags, rc):
        global connectionStatus
        print(rc)
        if rc == 0:
            connectionStatus = "connected"
            '''_running = True
            return _running'''
            

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.BuildApp()    
        
    def BuildApp(self):
        # configure the root window
        self.title('MQTT Explorer aber halt nd so gut')
        self.geometry('400x200')

        # label
        self.labelConnection = ttk.Label(self, text='You are connected to MQTT Broker: ' + broker_address, font=("Arial", 10))
        self.labelConnection.pack()

        self.labelConnectionStatus = ttk.Label(self, text="N/A")
        self.labelConnectionStatus.pack()

        self.labelSpacer = ttk.Label(self, text="===========================================")
        self.labelSpacer.pack()

        self.labelReceivedMsgData = ttk.Label(self, text="Sensor Reading: ")
        self.labelReceivedMsgData.pack()

        self.labelSpacer1 = ttk.Label(self, text="===========================================")
        self.labelSpacer1.pack()

        self.labelTopicLight = ttk.Label(self, text="Controll Topic: " + topicHouseMainLight)
        self.labelTopicLight.pack()

        # Button
        self.buttonPublishMsgOn = ttk.Button(self, text="ON")
        self.buttonPublishMsgOn['command'] = lambda: client.PublishMessage(topicHouseMainLight, "on")
        self.buttonPublishMsgOn.pack()

        self.buttonPublishMsgOff = ttk.Button(self, text="OFF")
        self.buttonPublishMsgOff['command'] = lambda: client.PublishMessage(topicHouseMainLight, "off")
        self.buttonPublishMsgOff.pack()
        

def TemperatureGenerator():
    sensorWert = random.randrange(25,45)
    client.PublishMessage(topicTemperaturSensor, sensorWert)
    

def loop():
    oldtime = time.time()
    
    while _running:
        while not q.empty():
            message = q.get()
            if message is None:
                continue
            else:
                app.labelReceivedMsgData.config(text="Sensor Reading: " + message.translate({98: None, 39: None}) + "°")
                                                                                            #Look up ASCII Table
                
        # tasks every 5 seconds
        if time.time() >= oldtime + 5:
            #=======randomTempGen=======
            oldtime = time.time()
            TemperatureGenerator()
            
            #=======OnConnectionStatus=======
            app.labelConnectionStatus.config(text="You are " + str(connectionStatus))

            #=======TkinterIdleTask=======
            #app.after(5000, app.update_idletasks())
            
        app.after(10, app.update())
        

def main():
    client.ReceiveMessage()
    loop()


#========object========#
app = Application()
client = Client()


if __name__ == "__main__":
    main()
