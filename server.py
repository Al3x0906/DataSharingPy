import socket
import threading
import os
import tqdm
import sys

SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, 0)
FORMAT = 'utf-8'
SEPARATOR=":"
BUFFER_SIZE = 4096
                    
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def file_path():
    fn = sys.argv
    fn.pop(0)
    return fn 
    
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected:  ")
    files=file_path()
    filepath=files[0]
    filesize = os.path.getsize(filepath)
    conn.send(f"{filepath}{SEPARATOR}{filesize}".encode(FORMAT))
    progress = tqdm.tqdm(range(filesize),f"Sending {filepath}" , unit ="B" , unit_scale=True , unit_divisor=1024)
    with open(filepath,"rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                progress.update(len(bytes_read))
                break
            conn.send(bytes_read)
            progress.update(len(bytes_read))
    conn_close(conn)


def conn_close(conn):
    print("\nConnection closed!!")
    conn.close()


def start(server):
    server.listen()
    print(f"[LISTENING] on {server.getsockname()}")
    while True:
        conn, addr = server.accept()
        # thread = threading.Thread(target=handle_client, args=(conn, addr))
        # thread.start()
        # print(f"[ACTIVE] {threading.active_count()-1} ")
        handle_client(conn, addr)


print("[STARTING] server is starting : ")

start(server)
