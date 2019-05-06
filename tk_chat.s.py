import tkinter as tk
import socket as sk
import threading as th
from time import sleep
import sys

def broadcast(msg, conn):
    for client in addrs:
        if client != conn:
            client.send(msg.encode('utf-8'))

def Enter_pressed(event):
    input_get = input_field.get()
    print(input_get)
    messages.insert(tk.INSERT, 'You: %s\n' % input_get)
    for client in addrs:
        client.send(input_get.encode('utf-8'))
    input_user.set('')

def handle_conn(conn):
    welcome = 'Welcome ! If you ever want to quit, type {Q} to exit.'
    conn.send(welcome.encode("utf-8"))
    while True:
        message = conn.recv(2048)
        if message != "{Q}":
            if len(message) != 0:
                message = "Client("+str(addrs[conn])+"): "+message.decode('utf-8')+"\n"
                messages.insert(tk.INSERT, message)
                broadcast(message, conn)
        else:
            conn.close()
            print('client disconnect')
            del addrs[conn]
            break

def recv_conn():
    while True:
        conn, addr = s.accept()
        print('Connected by', addr)
        addrs[conn] = addr
        th.Thread(target=handle_conn, args=(conn,)).start()

window = tk.Tk()
addrs = {}

window.title("Server")
messages = tk.Text(window)
messages.pack()

if len(sys.argv) != 3:
    print("Correct usage: script, IP address, port number")
    exit()

IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
s = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
s.bind((IP_address, Port))
s.listen()

input_user = tk.StringVar()
input_field = tk.Entry(window, text=input_user)
input_field.pack(side=tk.BOTTOM, fill=tk.X)

frame = tk.Frame(window)  # , width=300, height=300)
input_field.bind("<Return>", Enter_pressed)
frame.pack()

recv_th = th.Thread(target=recv_conn)
recv_th.start()
tk.mainloop()