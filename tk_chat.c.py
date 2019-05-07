import tkinter as tk
import socket as sk
import threading as th
from time import sleep
import sys

def Enter_pressed(event):
    input_get = input_field.get()
    input_user.set("")
    print(input_get)
    s.send(input_get.encode('utf-8'))
    messages.insert(tk.END, 'You: %s\n' % input_get)
    messages.itemconfigure(tk.END, background='lightgreen')
    if input_get == "{Q}":
        s.close()
        window.quit()

def recv():
    while True:
        # conn, addr = s.accept()
        try:
            message = s.recv(2048)
            if len(message)!=0:
                message = message.decode('utf-8')
                messages.insert(tk.END, message)
        except OSError: # left
            break

def on_closing():
    s.send("{Q}".encode('utf-8'))
    s.close()
    exit()

window = tk.Tk()
window.title("Client")
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


s = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
if len(sys.argv) != 3:
    print("Correct usage: script, IP address, port number")
    exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
s.connect((IP_address, Port))
print("Server(%s, %s) connected" % (IP_address, Port))

thread = th.Thread(target=recv)
thread.start()
window.protocol("WM_DELETE_WINDOW", on_closing)
tk.mainloop()