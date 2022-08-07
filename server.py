import socket
import threading
import os
import tqdm

PORT = 5001
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
SEPARATOR=":"
BUFFER_SIZE = 4096
                    
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected :")
    #Write Code to Send files here
    filename = "./filename.txt"
    filesize = os.path.getsize(filename)
    conn.send(f"{filename}{SEPARATOR}{filesize}".encode(FORMAT))
    progress = tqdm.tqdm(range(filesize),f"Sending {filename}" , unit ="B" , unit_scale=True , unit_divisor=1024)
    with open(filename,"rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                progress.update(len(bytes_read))
                break
            conn.send(bytes_read)
            progress.update(len(bytes_read))
        conn.close()


def start():
    server.listen(5)
    print(f"[LISTENING] on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE] {threading.active_count()-1} ")


print("[STARTING] server is starting : ")
start()
