from tkinter import *
import paho.mqtt.client as mqtt
import random


client = mqtt.Client()
onmessage = False

light = True


def clickSendMessage():
    topic = mygui.topicentry.get()
    message = mygui.messageentry.get()
    client.publish(topic, payload=message)
    print("Message sent!")


class MainWindow:
    def __init__(self, master):
        self.master = master
        master.title("MQTT-Broker")

        self.SendButton = Button(text="Send Message", command=clickSendMessage)

        self.topiclabel = Label(text="Topic:")
        self.topicentry = Entry()

        self.messagelabel = Label(text="Message:")
        self.messageentry = Entry()

        self.Listofmessage = Listbox(width=50)

        self.lightlabel = Label(text=" ", bg="#222233", padx=15, pady=15,)

        self.tempbutton = Button(text="Temperatursensor", command=temperature)

        self.tempbutton.grid(row=0, column=3)

        self.lightlabel.grid(row=1, column=3)

        self.SendButton.grid(row=2, column=1, pady=5)

        self.topiclabel.grid(row=0, column=0)
        self.messagelabel.grid(row=1, column=0)

        self.topicentry.grid(row=0, column=1)
        self.messageentry.grid(row=1, column=1)

        self.Listofmessage.grid(row=0, rowspan=4, column=2, padx=15, pady=20)


def temperature():
    rand = random.randrange(15, 39)
    client.publish("house/temperature/sensor1", payload=rand)


def updatemessage():
    mygui.Listofmessage.insert(
        0, "Topic: " + msgtopic + " ; Message: " + msgtext)


def on_message(client, userdata, msg):
    global msgtext
    global msgtopic
    global onmessage
    global light
    print(str(msg.payload.decode("utf-8")))
    msgtext = str(msg.payload.decode("utf-8"))
    msgtopic = msg.topic
    if msgtext == "on":
        light = True
    if msgtext == "off":
        light = False
    onmessage = True


client = mqtt.Client()
client.username_pw_set("lukas", password="lukas")
client.connect("172.104.234.24", 1883, 60)
print("Connected succesful!")
client.on_message = on_message
client.subscribe("#")
client.loop_start()


root = Tk()
mygui = MainWindow(root)


def main():
    print()


if __name__ == '__main__':
    main()

while True:
    root.update_idletasks()
    root.update()
    if onmessage:
        updatemessage()
        onmessage = False
        if light:
            mygui.lightlabel.config(bg="#fff883")
            print("True")
        elif not light:
            mygui.lightlabel.config(bg="#222233")
            print("False")
