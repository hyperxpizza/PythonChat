#modules for socket + tkinter GUI
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
#python2 or python3
try:                        
    from tkinter import *
except:
    from Tkinter import *
from datetime import datetime
import sys

#recieving messages
def recieve_messages():
    while True:
        try:
            msg = clientSocket.recv(bufforSize)
            msgList.insert("end", msg)
        #client leaving the chat
        except OSError:
            break

#sending messages
def send_message(event=None):
    msg = myMsg.get()
    msg += str(datetime.now()) + " "
    myMsg.set("")
    clientSocket.send(bytes((msg), "utf8"))
    if msg == "{quit}":
        clientSocket.close()
        root.quit()

#when window is closed
def closed(event=None):
    myMsg.set("{quit}")
    send_message()

def exit_chat():
    sys.exit()

root = Tk()
root.title("Chat")

#GUI properties
msgFrame = Frame(root)
myMsg = StringVar()
scroll = Scrollbar(msgFrame) #to scroll through messages
msgList = Listbox(msgFrame, height=15, width=300, yscrollcommand=scroll.set)
scroll.pack(side=RIGHT, fill=Y)
msgList.pack(side=LEFT, fill=BOTH)
msgList.pack()
msgFrame.pack()

msgField = Entry(root, textvariable=myMsg)
msgField.bind("<Return>", send_message)
msgField.pack()
send_btn = Button(root, text="Send", command=send_message)
send_btn.pack()
exit_btn = Button(root, text="Exit", fg="red", command=exit_chat)
exit_btn.pack()

root.protocol("WM_DELETE_WINDOW", closed)

#sockets

host = input("Enter Host: ")
port = input("Enter Port: ")

if not port:
    port = 33000
else:
    port = int(port)

bufforSize = 1024
addr = (host,port)

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(addr)

recieveThread = Thread(target=recieve_messages)
recieveThread.start()
root.mainloop()


