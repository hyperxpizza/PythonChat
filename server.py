#modules
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from variables import *

#server
server = socket(AF_INET, SOCK_STREAM)
server.bind(addr)

#add incoming clients
def add_incoming_clients():
    while True:
        client, client_adress = server.accept()
        print(str(client_adress) + " has connected!")
        client.send(bytes("Witaj na FokeChat! Wpisz swoj nick i wcisnij Enter!", "utf8"))

        #add new client adress to the list
        adresses[client] = client_adress
        Thread(target=deal_with_client, args=(client,)).start()

def deal_with_client(client):
    name = client.recv(bufforSize).decode("utf8")
    welcomeMsg = 'Witaj %s! Jesli chcesz wyjsc, wpisz {quit}' % name

    #send a welcome message
    client.send(bytes(welcomeMsg, "utf8"))
    joinedMsg = "%s dolaczyl/a do FokeChatu!" % name
    boardcast(bytes(joinedMsg,"utf8"))

    #add a client to clients list
    clients[client] = name
    
    while True:
        msg = client.recv(bufforSize)
        if msg != bytes("{quit}", "utf8"):
            boardcast(msg, name+": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            boardcast(bytes(name + " has left the chat :("))
            break       

def boardcast(msg, prefix=""):
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg) 


if __name__ == "__main__":
    server.listen(5)
    print("Wainting for connection...")
    accept_thread = Thread(target=add_incoming_clients)
    accept_thread.start()
    accept_thread.join()
    server.close()