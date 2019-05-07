import tkinter as tk
import socket as sk
import threading as th
from time import sleep
import getopt
import sys

def broadcast(msg, conn):
    for client in addrs:
        if client != conn:
            client.send(msg.encode('utf-8'))

def Enter_pressed(event):
    input_get = input_field.get()
    print(input_get)
    messages.insert(tk.END, 'You: %s\n' % input_get)
    messages.itemconfigure(tk.END, background='lightgreen')
    for client in addrs:
        client.send(("Server: "+input_get).encode('utf-8'))
    input_user.set('')

def handle_conn(conn):
    welcome = 'Server: Welcome ! If you ever want to quit, type {Q} to exit.\n'
    conn.send(welcome.encode("utf-8"))
    while True:
        message = conn.recv(2048)
        if len(message) != 0:
            message = message.decode('utf-8')
            if message != "{Q}":
                    message = "Client("+str(addrs[conn])+"): "+message+"\n"
                    if not cli:
                        messages.insert(tk.END, message)
                    broadcast(message, conn)
            else:
                conn.close()
                print('client(%s) disconnect' % str(addrs[conn]))
                del addrs[conn]
                break

def recv_conn():
    while True:
        conn, addr = s.accept()
        print('Connected by', addr)
        addrs[conn] = addr
        th.Thread(target=handle_conn, args=(conn,)).start()

addrs = {}
cli = False
IP_address = '0.0.0.0'
Port = 8888

try:
    window = tk.Tk()

    window.title("Server")
    frame = tk.Frame(window)  # , width=300, height=300)
    scrollbar = tk.Scrollbar(frame)
    messages = tk.Listbox(frame, width=50, height=15, yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    messages.pack(side=tk.LEFT, fill=tk.BOTH)
    frame.pack()

    input_user = tk.StringVar()
    input_field = tk.Entry(window, text=input_user)
    input_field.pack(side=tk.BOTTOM, fill=tk.X)

    input_field.bind("<Return>", Enter_pressed)
except tk.TclError:
    cli = True

try:
    opts, args = getopt.getopt(sys.argv[1:], "a:p:c", ["addr", "port"])
except getopt.GetoptError as err:
    print(str(err))
    print("Usage: python th_chat.s.py -a<ip_address> -p<port_number> -c")
for o, a in opts:
    if o == "-c":
        cli = True
    elif o in ("-a", "--addr"):
        IP_address = str(a)
    elif o in ("-p", "--port"):
        Port = int(a)

s = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
s.bind((IP_address, Port))
s.listen()

if not cli:
    th.Thread(target=recv_conn).start()
    tk.mainloop()
else:
    recv_conn()