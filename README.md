## Simple chat program by tkinter and socket

### Function:
- Server and clients are in one chatroom, they can chat with each other

### Dependence:
- Python3
- socket
- threading
- tkinter

### usage:
- Server:
  - python tk_chat.s.py -a&lt;address&gt; -p&lt;port&gt; -c
    - if you want to chat through internet, address must be `0.0.0.0` (or you don't need to appoint address, and port is `8888` by default)
    - if with graph, server can broadcast message.
    - `-c` is for no graph, and if you start it with no display variable, program will also enter nograph mode.

- Client:
  - python tk_chat.c.py &lt;server_address&gt; &lt;server_port&gt;
  - need to appoint a nick name, if no, server will set it to your ip and port.